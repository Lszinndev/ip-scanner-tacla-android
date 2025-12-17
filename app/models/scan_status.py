from enum import Enum


class ScanStatus(str, Enum):
    HOST_DOWN = "host_down"
    TIMEOUT = "timeout"
    REFUSED = "refused"
    UP = "up"
    ERROR = "error"
