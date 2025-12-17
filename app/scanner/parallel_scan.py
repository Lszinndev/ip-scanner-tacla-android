from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from app.scanner.ip_scanner import scan_ip
from app.scanner.ping import ping_host


def scan_ips_parallel(ips: List[str], port: int, max_workers: int = 10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}

        for ip in ips:
            futures[executor.submit(ping_host, ip)] = ip

        alive_hosts = []

        for future in as_completed(futures):
            ip = futures[future]
            if future.result():
                alive_hosts.append(ip)
            else:
                results.append({
                    "ip": ip,
                    "port": port,
                    "status": "host_down",
                    "response_time_ms": None
                })

        port_futures = [
            executor.submit(scan_ip, ip, port)
            for ip in alive_hosts
        ]

        for future in as_completed(port_futures):
            results.append(future.result())

    return results
