from enum import Enum


class OrderStrategy(str, Enum):
    QUANTITY = "QUANTITY"
    VALUE = "VALUE"

    def __str__(self) -> str:
        return str(self.value)
