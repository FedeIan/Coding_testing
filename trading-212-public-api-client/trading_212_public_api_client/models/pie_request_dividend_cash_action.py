from enum import Enum


class PieRequestDividendCashAction(str, Enum):
    REINVEST = "REINVEST"
    TO_ACCOUNT_CASH = "TO_ACCOUNT_CASH"

    def __str__(self) -> str:
        return str(self.value)
