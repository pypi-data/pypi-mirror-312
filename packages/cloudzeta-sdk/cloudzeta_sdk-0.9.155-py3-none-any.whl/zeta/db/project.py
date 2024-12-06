from zeta.db import BaseData, NestedZetaBase
from dataclasses import dataclass


@dataclass
class ZetaProjectData(BaseData):
    storagePath: str

    isPublic: bool
    isPublished: bool
    roles: dict[str, str]

class ZetaProject(NestedZetaBase):
    @property
    def collection_name(self) -> str:
        return "projects"

    @property
    def parent_uid_field(cls) -> str:
        return "user_uid"

    @property
    def data_class(self):
        return ZetaProjectData

    def get_session_storage_path(self, session_uid: str) -> str:
        if not self.data.storagePath.endswith("/main"):
            raise ValueError(f"Invalid project storage path: {self.data.storagePath}")

        # Replace "/main" with f"/{session_id}"
        return self.data.storagePath[:-5] + f"/{session_uid}"