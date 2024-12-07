from enum import Enum


class COUNTERDatasetIdentifiersType(str, Enum):
    DOI = "doi"
    PROPRIETARY = "proprietary"
    URI = "uri"

    def __str__(self) -> str:
        return str(self.value)
