from enum import Enum


class COUNTERDatasetDatesType(str, Enum):
    FIRST_ACCESSED_ONLINE = "first-accessed-online"
    PROPRIETARY = "proprietary"
    PUB_DATE = "pub-date"

    def __str__(self) -> str:
        return str(self.value)
