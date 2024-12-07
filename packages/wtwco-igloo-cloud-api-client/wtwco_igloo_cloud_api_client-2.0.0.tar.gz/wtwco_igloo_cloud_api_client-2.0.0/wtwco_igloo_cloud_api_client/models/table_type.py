from enum import Enum


class TableType(str, Enum):
    INPUTLIST = "InputList"
    INPUTTABLE = "InputTable"
    RESULTTABLE = "ResultTable"

    def __str__(self) -> str:
        return str(self.value)
