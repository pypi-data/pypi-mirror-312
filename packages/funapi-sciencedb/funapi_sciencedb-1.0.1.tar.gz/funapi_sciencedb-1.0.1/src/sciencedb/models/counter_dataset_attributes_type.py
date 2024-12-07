from enum import Enum


class COUNTERDatasetAttributesType(str, Enum):
    DATASET_TYPE = "dataset=-type"
    DATASET_VERSION = "dataset-version"
    PROPRIETARY = "proprietary"

    def __str__(self) -> str:
        return str(self.value)
