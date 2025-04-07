from fastapi import APIRouter, Depends
from redis import Redis
from rq import Queue
from rq.job import Job

router = APIRouter(prefix="/search-index", tags=["Search Index"])

redis_conn = Redis(host="redis", port=6379)  # Configuração do Redis
queue = Queue(connection=redis_conn)  # Fila do RQ Worker

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    job = Job.fetch(task_id, connection=redis_conn)  # Busca a job no Redis
    return {
        "task_id": task_id,
        "status": job.get_status(),  # Retorna o status da task
        "result": job.result  # Se já tiver resultado, retorna também
    }
