from enum import Enum


class SUSHIErrorModelSeverity(str, Enum):
    DEBUG = "Debug"
    FATAL = "Fatal"
    INFO = "Info"
    WARNING = "Warning"

    def __str__(self) -> str:
        return str(self.value)
