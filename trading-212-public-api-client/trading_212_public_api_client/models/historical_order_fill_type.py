from enum import Enum


class HistoricalOrderFillType(str, Enum):
    OTC = "OTC"
    TOTV = "TOTV"

    def __str__(self) -> str:
        return str(self.value)
