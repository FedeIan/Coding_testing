from enum import Enum


class ReportResponseStatus(str, Enum):
    CANCELED = "Canceled"
    FAILED = "Failed"
    FINISHED = "Finished"
    PROCESSING = "Processing"
    QUEUED = "Queued"
    RUNNING = "Running"

    def __str__(self) -> str:
        return str(self.value)
