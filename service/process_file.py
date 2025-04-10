from typing import List

from fastapi import UploadFile
from service.extraction_and_cleaning.transform_pdf_in_txt import extrair_texto_pdf
from service.worker import process_pdf_task
from util.generate_string import generate_unique_filename
from redis import Redis
from rq import Queue
from pathlib import Path
import shutil

redis_conn = Redis(host="localhost", port=6379)
fila = Queue(connection=redis_conn)

async def process_pdf(files: List[UploadFile]):
    saved_files = []
    print(f"Processando {len(files)} arquivos...")

    for file in files:
        try:
            file_name_unique = generate_unique_filename()
            filename_hash = f"{file_name_unique}.{file.content_type.split('/')[1]}"

            save_path = Path(f"data/files/{filename_hash}")
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_files.append({
                "file_path": str(save_path),
                "file_name_unique": filename_hash,
                "original_name": file.filename,
                "content_type": file.content_type,
            })

        except Exception as e:
                return {"Falha ao processar arquivos": {str(e)}}

    job = fila.enqueue(process_pdf_task, saved_files, job_timeout=-1)
    return {"job_id": job.get_id()}