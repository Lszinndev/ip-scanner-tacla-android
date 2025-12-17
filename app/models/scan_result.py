from pydantic import BaseModel
from typing import Optional
from app.models.scan_status import ScanStatus


class ScanResult(BaseModel):
    ip: str
    port: int
    status: ScanStatus
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
