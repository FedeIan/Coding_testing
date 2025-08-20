from enum import Enum


class HistoryTransactionItemType(str, Enum):
    DEPOSIT = "DEPOSIT"
    FEE = "FEE"
    TRANSFER = "TRANSFER"
    WITHDRAW = "WITHDRAW"

    def __str__(self) -> str:
        return str(self.value)
