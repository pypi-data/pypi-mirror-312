from enum import Enum


class TaskStatus(Enum):
    QUEUED = "Queued"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILURE = "Failure"
    SKIPPED = "Skipped"
