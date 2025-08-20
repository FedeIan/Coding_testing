from enum import Enum


class HistoricalOrderExecutor(str, Enum):
    ANDROID = "ANDROID"
    API = "API"
    AUTOINVEST = "AUTOINVEST"
    IOS = "IOS"
    SYSTEM = "SYSTEM"
    WEB = "WEB"

    def __str__(self) -> str:
        return str(self.value)
