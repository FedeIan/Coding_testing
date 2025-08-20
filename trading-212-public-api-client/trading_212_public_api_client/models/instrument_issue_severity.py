from enum import Enum


class InstrumentIssueSeverity(str, Enum):
    INFORMATIVE = "INFORMATIVE"
    IRREVERSIBLE = "IRREVERSIBLE"
    REVERSIBLE = "REVERSIBLE"

    def __str__(self) -> str:
        return str(self.value)
