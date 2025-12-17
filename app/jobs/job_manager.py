import uuid
import time
from typing import Dict, List
from enum import Enum
from app.models.scan_result import ScanResult


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class ScanJob:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.status = JobStatus.PENDING
        self.result: List[ScanResult] = []
        self.error: str | None = None

        self.total: int = 0
        self.completed: int = 0

        self.created_at = time.time()


jobs: Dict[str, ScanJob] = {}
