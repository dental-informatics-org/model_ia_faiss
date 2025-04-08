from fastapi import APIRouter, Query
from redis import Redis
from rq import Queue
from rq.job import Job

router = APIRouter(prefix="/search-index", tags=["Search Index"])

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

@router.get("/task-status")
def check_job_status(job_id: str = Query(..., description="ID do job RQ")):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        
        response = {
            "status": job.get_status()
        }

        if job.is_finished:
            response["result"] = job.result
        
        elif job.is_failed:
            response["error"] = str(job.exc_info)

        return response
    
    except Exception as e:
        return {"error": f"Job ID inválido ou não encontrado. Detalhes: {str(e)}"}
