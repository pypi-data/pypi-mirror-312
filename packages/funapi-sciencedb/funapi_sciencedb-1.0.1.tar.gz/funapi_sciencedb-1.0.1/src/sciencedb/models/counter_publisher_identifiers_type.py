from enum import Enum


class COUNTERPublisherIdentifiersType(str, Enum):
    GRID = "GRID"
    ISNI = "ISNI"
    ORCID = "ORCID"

    def __str__(self) -> str:
        return str(self.value)
