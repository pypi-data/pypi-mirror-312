from enum import Enum


class COUNTERDatasetContributorsType(str, Enum):
    ISNI = "isni"
    NAME = "name"
    ORCID = "orcid"

    def __str__(self) -> str:
        return str(self.value)
