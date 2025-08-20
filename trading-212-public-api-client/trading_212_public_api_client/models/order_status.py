from enum import Enum


class OrderStatus(str, Enum):
    CANCELLED = "CANCELLED"
    CANCELLING = "CANCELLING"
    CONFIRMED = "CONFIRMED"
    FILLED = "FILLED"
    LOCAL = "LOCAL"
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    REJECTED = "REJECTED"
    REPLACED = "REPLACED"
    REPLACING = "REPLACING"
    UNCONFIRMED = "UNCONFIRMED"

    def __str__(self) -> str:
        return str(self.value)
