from dataclasses import dataclass
from enum import Enum


class StorageVendor(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


@dataclass
class StorageConfig(object):
    vendor: StorageVendor
    url: str

    def to_dict(self):
        return {
            "vendor": self.vendor.value,
            "bucketUrl": self.bucketUrl,
        }