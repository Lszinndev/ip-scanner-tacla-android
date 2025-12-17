import socket
import time
from typing import Dict


def scan_ip(ip: str, port: int, timeout: float = 1.0) -> Dict:
    result = {
        "ip": ip,
        "port": port,
        "status": "down",
        "response_time_ms": None
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    start = time.perf_counter()

    try:
        sock.connect((ip, port))
        end = time.perf_counter()

        result["status"] = "up"
        result["response_time_ms"] = round((end - start) * 1000, 2)

    except socket.timeout:
        result["status"] = "timeout"

    except ConnectionRefusedError:
        result["status"] = "refused"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    finally:
        sock.close()

    return result
