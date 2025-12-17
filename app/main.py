from fastapi import FastAPI, Query, HTTPException
from typing import List
from concurrent.futures import ThreadPoolExecutor
from app.jobs.cleanup import cleanup_jobs
from app.models.scan_result import ScanResult
from app.jobs.job_manager import ScanJob, jobs
from app.jobs.scan_worker import run_scan_job
from fastapi import Header, Depends

API_KEY = "super-secret-key"
API_KEY_HEADER = "X-API-Key"


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")


executor = ThreadPoolExecutor(max_workers=5)
MAX_IP_RANGE = 100

app = FastAPI(title="IP Scanner API")

@app.middleware("http")
async def job_cleanup_middleware(request, call_next):
    cleanup_jobs()
    response = await call_next(request)
    return response



@app.get("/")
def root():
    return {"status": "API rodando"}


@app.post("/scan")
def create_scan(
    start_ip: str = Query(...),
    end_ip: str = Query(...),
    port: int = Query(..., ge=1, le=65535),
    _: None = Depends(verify_api_key)
    
):
    job = ScanJob()
    jobs[job.id] = job

    executor.submit(
        run_scan_job,
        job,
        start_ip,
        end_ip,
        port
    )

    return {
        "scan_id": job.id,
        "status": job.status
    }


@app.get("/scan/{scan_id}/status")
def scan_status(scan_id: str):
    job = jobs.get(scan_id)
    _: None = Depends(verify_api_key)

    if not job:
        raise HTTPException(status_code=404, detail="Scan não encontrado")

    return {
        "scan_id": job.id,
        "status": job.status
    }


@app.get("/scan/{scan_id}/result", response_model=List[ScanResult])
def scan_result(scan_id: str):
    job = jobs.get(scan_id)
    _: None = Depends(verify_api_key)

    if not job:
        raise HTTPException(status_code=404, detail="Scan não encontrado")

    if job.status != "done":
        raise HTTPException(
            status_code=400,
            detail=f"Scan ainda não finalizado. Status atual: {job.status}"
        )

    return job.result

@app.get("/scan/{scan_id}/progress")
def scan_progress(scan_id: str):
    job = jobs.get(scan_id)
    _: None = Depends(verify_api_key)

    if not job:
        raise HTTPException(status_code=404, detail="Scan não encontrado")

    percent = 0
    if job.total > 0:
        percent = round((job.completed / job.total) * 100, 2)

    return {
        "scan_id": job.id,
        "status": job.status,
        "completed": job.completed,
        "total": job.total,
        "progress_percent": percent
    }
