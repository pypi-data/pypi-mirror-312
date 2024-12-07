from enum import Enum


class COUNTERDatasetUsageDataType(str, Enum):
    DATASET = "Dataset"

    def __str__(self) -> str:
        return str(self.value)
