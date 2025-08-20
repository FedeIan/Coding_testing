from enum import Enum


class AccountBucketResultResponseStatus(str, Enum):
    AHEAD = "AHEAD"
    BEHIND = "BEHIND"
    ON_TRACK = "ON_TRACK"

    def __str__(self) -> str:
        return str(self.value)
