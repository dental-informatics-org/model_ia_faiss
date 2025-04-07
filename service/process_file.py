from fastapi import UploadFile
from typing import List
from service.extraction_and_cleaning.transform_pdf_in_txt import extrair_texto_pdf
from service.worker import process_pdf_task
from util.generate_string import generate_unique_filename, get_file_hash
from redis import Redis
from rq import Queue

redis_conn = Redis(host="redis", port=6379)
fila = Queue(connection=redis_conn)

async def process_pdf(files: List[UploadFile]):
    files_data = []
    for file in files:
        file_hash = await get_file_hash(file)
        file_name_unique = generate_unique_filename()
        text = await extrair_texto_pdf(file, file_name_unique)

        files_data.append({
            "hash": file_hash,
            "filename": file_name_unique,
            "text": text
        })
    job = fila.enqueue(process_pdf_task, files_data)

    return {"job_id": job.get_id()}