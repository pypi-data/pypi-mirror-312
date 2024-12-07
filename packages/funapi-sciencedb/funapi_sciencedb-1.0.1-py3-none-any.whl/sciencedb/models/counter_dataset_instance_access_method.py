from enum import Enum


class COUNTERDatasetInstanceAccessMethod(str, Enum):
    MACHINE = "machine"
    REGULAR = "regular"

    def __str__(self) -> str:
        return str(self.value)
