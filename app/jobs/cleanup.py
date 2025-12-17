import time
from app.jobs.job_manager import jobs

JOB_TTL_SECONDS = 300  # 5 minutos


def cleanup_jobs():
    now = time.time()
    expired = []

    for job_id, job in jobs.items():
        if now - job.created_at > JOB_TTL_SECONDS:
            expired.append(job_id)

    for job_id in expired:
        del jobs[job_id]
