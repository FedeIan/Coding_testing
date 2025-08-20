from enum import Enum


class HistoricalOrderTimeValidity(str, Enum):
    DAY = "DAY"
    GOOD_TILL_CANCEL = "GOOD_TILL_CANCEL"

    def __str__(self) -> str:
        return str(self.value)
