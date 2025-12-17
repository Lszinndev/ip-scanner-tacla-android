import ipaddress
from typing import List


def generate_ip_range(start_ip: str, end_ip: str) -> List[str]:
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    if start > end:
        raise ValueError("IP inicial maior que IP final")

    return [
        str(ipaddress.IPv4Address(ip))
        for ip in range(int(start), int(end) + 1)
    ]
