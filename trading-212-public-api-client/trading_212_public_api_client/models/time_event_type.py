from enum import Enum


class TimeEventType(str, Enum):
    AFTER_HOURS_CLOSE = "AFTER_HOURS_CLOSE"
    AFTER_HOURS_OPEN = "AFTER_HOURS_OPEN"
    BREAK_END = "BREAK_END"
    BREAK_START = "BREAK_START"
    CLOSE = "CLOSE"
    OPEN = "OPEN"
    OVERNIGHT_OPEN = "OVERNIGHT_OPEN"
    PRE_MARKET_OPEN = "PRE_MARKET_OPEN"

    def __str__(self) -> str:
        return str(self.value)
