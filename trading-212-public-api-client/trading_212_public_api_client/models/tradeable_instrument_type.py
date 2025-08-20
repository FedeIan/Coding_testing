from enum import Enum


class TradeableInstrumentType(str, Enum):
    CORPACT = "CORPACT"
    CRYPTO = "CRYPTO"
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    CVR = "CVR"
    ETF = "ETF"
    FOREX = "FOREX"
    FUTURES = "FUTURES"
    INDEX = "INDEX"
    STOCK = "STOCK"
    WARRANT = "WARRANT"

    def __str__(self) -> str:
        return str(self.value)
