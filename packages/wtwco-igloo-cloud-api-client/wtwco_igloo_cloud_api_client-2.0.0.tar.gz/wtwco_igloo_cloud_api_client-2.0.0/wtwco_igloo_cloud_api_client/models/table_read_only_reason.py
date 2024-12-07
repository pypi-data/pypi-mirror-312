from enum import Enum


class TableReadOnlyReason(str, Enum):
    NONE = "None"
    NOTCALCULATED = "NotCalculated"
    RESULT = "Result"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return str(self.value)
