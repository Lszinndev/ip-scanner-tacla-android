from app.jobs.job_manager import ScanJob, JobStatus
from app.scanner.ip_range import generate_ip_range
from app.scanner.parallel_scan import scan_ips_parallel


def run_scan_job(
    job: ScanJob,
    start_ip: str,
    end_ip: str,
    port: int
):
    try:
        job.status = JobStatus.RUNNING

        ips = generate_ip_range(start_ip, end_ip)
        job.total = len(ips)

        results = scan_ips_parallel(ips, port)

        job.result = results
        job.completed = job.total
        job.status = JobStatus.DONE

    except Exception as e:
        job.status = JobStatus.ERROR
        job.error = str(e)
