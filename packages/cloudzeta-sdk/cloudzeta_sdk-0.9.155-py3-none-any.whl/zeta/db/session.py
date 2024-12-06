from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from postgrest.exceptions import APIError
import os
import re

from pxr import Sdf, Usd, Tf

from zeta.converter.base import ConvertData, BaseConverter
from zeta.converter.fbx import FbxConverter
from zeta.converter.gltf import GltfConverter
from zeta.converter.obj import ObjConverter
from zeta.converter.usdz import UsdzConverter
from zeta.db import BaseData, ZetaBase, ZetaBaseBackend
from zeta.db.layer import ZetaLayer
from zeta.db.project import ZetaProject
from zeta.db.user import ZetaUser
from zeta.sdk.asset import AssetUtils
from zeta.sdk.uid import generate_uid
from zeta.storage.base import BlobListResponse, StorageBucket
from zeta.usd.resolve import ResolverContext
from zeta.utils.downloader import AssetDownloader
from zeta.utils.logging import zetaLogger


class ZetaSessionState(Enum):
    """
    The state of the session
    """
    INIT = "init"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


@dataclass
class ZetaSessionData(BaseData):
    projectUid: str
    rootAssetPath: str
    externalAssetPath: str
    assetPrefix: list[str]

    # If true, the session will be public and readable to all registered users.
    isPublic: bool

    # If true, the session will be published the the Internet and readable to all users who have
    # a link to the session.
    isPublished: bool

    # Ephemeral sessions do not need a registered user to create.
    #
    # If true, the session will be automatically deleted in a certain period of time after it
    # becomes inactive.
    isEphemeral: bool

    roles: dict[str, str]
    state: ZetaSessionState;

    annotationLayerUid: str;
    editLayerUid: str;

    error: str;
    thumbnailAsset: str;
    usdzAssetPath: str;


class ZetaSession(ZetaBase):
    _max_asset_retry: int = 1024

    def __init__(self):
        super().__init__()

        self._stage: Usd.Stage = None

        self._workspace: str = None
        self._owner: ZetaUser = None
        self._bucket: StorageBucket = None
        self._project: ZetaProject = None
        self._resolver_context: ResolverContext = None
        self._edit_layer: ZetaLayer = None

    @property
    def collection_name(cls) -> str:
        return "sessions"

    @property
    def data_class(self):
        return ZetaSessionData

    @property
    def stage(self) -> Usd.Stage:
        return self._stage

    @property
    def root_asset_blobname(self) -> str:
        assert self._project is not None, "Project not loaded"

        # Note that we can't use os.path.join here because root_asset_path is an absolute path.
        return os.path.normpath(f"{self._project.data.storagePath}/{self._data.rootAssetPath}")

    @property
    def owner_uid(self) -> str:
        owners = [uid for uid, role in self._data.roles.items() if role == "owner"]
        if len(owners) == 0:
            raise ValueError("Owner not found")
        if len(owners) > 1:
            raise ValueError("Multiple owners found")
        return owners[0]

    def _data_from_dict(self, data: dict):
        super()._data_from_dict(data)

        if self._data and type(self._data.state) == str:
            self._data.state = ZetaSessionState(self._data.state)

    def _push_edit_layer_updates(self, *args):
        self._edit_layer.push_updates()

    def _update_state_firebase(self, from_state: str, to_state: str) -> bool:
        with self._db.transaction(max_attempts=1):
            session_data = self._ref.get()
            state: str = session_data.get("state")

            if (state != from_state):
                zetaLogger.error(f"invalid state transition: {self._uid}, state={state}")
                return False

            self.update({ "state": to_state })
            return True

    def _update_state_supabase(self, from_state: str, to_state: str) -> bool:
        try:
            self._table.update({
                "state": to_state,
                "updated_at": self._get_current_time(),
            }).eq("uid", self._uid).eq("state", from_state).execute()

            record = self._table.select("*").eq("uid", self._uid).single().execute().data
            self._data_from_dict(record)
        except APIError as e:
            zetaLogger.error(f"Failed to update state: {self._uid}, state={from_state}, code={e.code}")
            return False

        return True

    def update_state(self, from_state: ZetaSessionState, to_state: ZetaSessionState) -> bool:
        assert self.valid, "Invalid session object."

        if self.backend == ZetaBaseBackend.FIREBASE:
            return self._update_state_firebase(from_state.value, to_state.value)
        elif self.backend == ZetaBaseBackend.SUPABASE:
            return self._update_state_supabase(from_state.value, to_state.value)
        else:
            raise ValueError(f"Invalid backend: {self.backend}")

    def update_error(self, error: str) -> None:
        self.update({
            "error": error,
        })

    def _init_resolver_context(self):
        assert self._workspace is None, "Workspace already initialized"
        self._workspace = f"/tmp/{generate_uid()}"

        assert self._owner is None, "Owner already loaded"
        self._owner = ZetaUser.get_by_uid(self.owner_uid)

        if not AssetDownloader.has_engine():
            # When asset downloader deoes not come with ZetaEngine, We are running in the server
            # backend. We need to initialize the asset downloader with the engine.
            assert self._bucket is None, "Bucket already loaded"
            try:
                self._bucket = StorageBucket.get_bucket(self._owner.storage)
            except ValueError as e:
                zetaLogger.error(f"Failed to get bucket: {e}")

        assert self._project is None, "Project already loaded"
        self._project = ZetaProject.get_from_parent_collection(self._owner, self._data.projectUid)

        # Validate the project storage path
        project_match = re.match(r"^users/([^/]+)/projects/([^/]+)/([^/]+)$",
                                 self._project.data.storagePath)
        assert project_match, f"Invalid project storage path: {self._project.data.storagePath}"

        owner_uid, project_uid, _ = project_match.groups()
        assert owner_uid == self._owner.uid, f"Invalid project storage path: {self._project.data.storagePath}"
        assert project_uid == self._project.uid, f"Invalid project storage path: {self._project.data.storagePath}"

        assert self._resolver_context is None, "Session already loaded"
        root_dir: str = os.path.dirname(self.root_asset_blobname)
        self._resolver_context = ResolverContext(root_dir, self._workspace)

    def load_stage(self) -> Usd.Stage:
        """
        Load the session into an OpenUSD stage.

        @param workspace (optional): The workspace directory where the asssets will be downloaded.
                                     If None, a temporary directory will be automatically created.
        @return: The OpenUSD stage.
        """
        if self._stage is not None:
            zetaLogger.warning("Session already loaded")
            return self._stage

        self._init_resolver_context()
        self._edit_layer = ZetaLayer.get_from_parent_collection(self, self._data.editLayerUid)

        if self._edit_layer is None:
            raise ValueError("Edit layer is not found")

        self._edit_layer.load_layer()
        if self._edit_layer.layer is None:
            raise ValueError("Edit layer is not loaded")

        root_asset_filename: str = AssetDownloader.download_asset(self.root_asset_blobname,
                                                                  self._workspace)

        self._stage = Usd.Stage.Open(root_asset_filename, self._resolver_context)
        if self._stage is None:
            raise ValueError("Stage is not loaded")

        session_layer: Sdf.Layer = self._stage.GetSessionLayer()
        if session_layer is None:
            raise ValueError("Session layer is not found")

        session_layer.subLayerPaths.append(self._edit_layer.layer.identifier)
        self._stage.SetEditTarget(self._edit_layer.layer)

        self._listener = Tf.Notice.Register(
            Usd.Notice.StageContentsChanged,
            self._push_edit_layer_updates,
            self._stage)

        return self._stage

    def _blob_prefix_exists(self, blob_prefix: str) -> bool:
        blobs: BlobListResponse = self._bucket.list_blobs(blob_prefix)
        return not blobs.is_empty()

    def _get_asset_prefix(self, root_asset_path, external_asset_path) -> list:
        unique_prefixes = set()

        unique_prefixes.add(root_asset_path)
        unique_prefixes.update(AssetUtils.get_all_parent_paths(root_asset_path))

        if external_asset_path is not None:
            unique_prefixes.add(external_asset_path)
            unique_prefixes.update(AssetUtils.get_all_parent_paths(external_asset_path))

        return list(unique_prefixes)

    def _get_session_storage_path(self, session_uid: str) -> str:
        project_storage_path: str = self._project.data.storagePath

        if not project_storage_path.endswith("/main"):
            raise ValueError(f"Invalid project storage path: {project_storage_path}")

        # Replace "/main" with f"/{session_id}"
        return project_storage_path[:-5] + f"/{session_uid}"

    def process_convert(self):
        self._init_resolver_context()

        zetaLogger.info(f"Converting for session {self._uid}, tmp path {self._workspace}")

        session_state = self.data.state
        if (session_state != ZetaSessionState.PROCESSING):
            raise ValueError(f"session is not in processing state, state={session_state}")

        root_asset_filename = AssetDownloader.download_asset(self.root_asset_blobname,
                                                             self._workspace)

        converter: BaseConverter = None

        if AssetUtils.is_unpacked_usd_asset(self.data.rootAssetPath):
            zetaLogger.info(f"Already in USD format, no need to convert: {self.data.rootAssetPath}")
            return
        elif AssetUtils.is_fbx_asset(self.data.rootAssetPath):
            converter = FbxConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_gltf_asset(self.data.rootAssetPath):
            converter = GltfConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_obj_asset(self.data.rootAssetPath):
            converter = ObjConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_usdz_asset(self.data.rootAssetPath):
            converter = UsdzConverter(self._workspace, root_asset_filename, self._resolver_context)
        else:
            zetaLogger.warning(f"Unsupported file format: {self.data.rootAssetPath}")
            return

        assert converter is not None

        for attempt in range(self._max_asset_retry):
            try:
                data: ConvertData = converter.extract()
                break  # Success
            except FileNotFoundError as e:
                asset_filepath = Path(e.filename)
                tmp_filepath = Path(self._workspace)
                asset_blobname: str = asset_filepath.relative_to(tmp_filepath).as_posix()
                zetaLogger.warning(f"Retry #{attempt+1}, download missing asset {asset_blobname}")
                AssetDownloader.download_asset(asset_blobname, self._workspace)
        else:
            raise ValueError(f"Error: Failed to convert file {root_asset_filename}")

        # Find a new empty blob prefix to host all converted assets.
        is_usdz: bool = AssetUtils.is_usdz_asset(self.data.rootAssetPath)
        converted_base: str = (f"unpacked_{Path(self.data.rootAssetPath).stem}" if is_usdz else
                               f"converted_{Path(self.data.rootAssetPath).stem}")
        converted_name: str = converted_base
        converted_blob_prefix: str = os.path.normpath(os.path.join(
            os.path.dirname(self.root_asset_blobname),
            converted_name,
        ))

        attempt: int = 0
        while True:
            attempt += 1
            if not self._blob_prefix_exists(converted_blob_prefix):
                break

            converted_name = f"{converted_base}_{attempt}"
            converted_blob_prefix = os.path.normpath(os.path.join(
                os.path.dirname(self.root_asset_blobname),
                converted_name,
            ))

        for asset_name, asset_filename in data.assets.items():
            asset_blobname: str = os.path.normpath(os.path.join(
                converted_blob_prefix,
                asset_name,
            ))

            if AssetUtils.is_asset_file_valid(asset_filename):
                zetaLogger.info(f"Uploading asset: {asset_filename} -> {asset_blobname}")
                self._bucket.upload_blob(asset_filename, asset_blobname)
            else:
                zetaLogger.error(f"Invalid asset file: {asset_filename}")

        new_root_asset_path: str = os.path.join(
            os.path.dirname(self.data.rootAssetPath),
            converted_name,
            os.path.basename(data.root_layer),
        )

        asset_prefix = self._get_asset_prefix(new_root_asset_path, self.data.rootAssetPath)

        thumbnail_blobname: str = None
        if AssetUtils.is_asset_file_valid(data.thumbnail_path):
            thumbnail_blobname = os.path.join(
                self._get_session_storage_path(self._uid),
                "__thumbnails",
                os.path.basename(data.thumbnail_path))
            self._bucket.upload_blob(data.thumbnail_path, thumbnail_blobname)

        session_update = {
            "rootAssetPath": new_root_asset_path,
            "assetPrefix": asset_prefix,
            "thumbnailAsset": thumbnail_blobname,
        }

        # Create USDZ asset for all formats (expect for USDZ obviously)
        if data.usdz_asset is not None:
            new_usdz_asset_path: str = os.path.join(
                os.path.dirname(self.data.rootAssetPath),
                converted_name,
                os.path.basename(data.usdz_asset),
            )
            session_update["usdzAssetPath"] = new_usdz_asset_path

        self.update(session_update)