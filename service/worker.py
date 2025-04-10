import json
from pathlib import Path
from typing import List, Dict
from redis import Redis
from db_model.file import FileModel
from rq import Worker, Queue, get_current_job
from repository.file import mark_as_indexed, save_file_if_not_exists
from service.embeddings_and_index.embeddings_and_index import indexar_textos
from service.extraction_and_cleaning.clean_txt import limpar_texto
from service.extraction_and_cleaning.transform_pdf_in_txt import extrair_texto_pdf
from datetime import datetime

from util.generate_string import get_file_hash_from_path

redis_conn = Redis(host="localhost", port=6379)
fila = Queue(connection=redis_conn)

def process_pdf_task(files: List[Dict]) -> dict:
    job = get_current_job()
    job_id = job.id if job else None
    
    errors = []
    processed = []
    for file in files:
        if redis_conn.get(f"cancel_job:{job_id}") == b"1":
            errors.append(f"Job {job_id} cancelado manualmente.")
            break
        try:
            file_path = Path(file["file_path"])
            file_name_unique = file["file_name_unique"]
            original_name = file["original_name"]
            content_type = file["content_type"]
            file_hash = get_file_hash_from_path(str(file_path))

            save = save_in_db(file_path, file_name_unique, original_name, content_type, file_hash)
            file_data = save.get("data")

            if save["status"] == "skipped":
                if not file_data or file_data.is_indexed:
                    reason = save.get("reason", "Arquivo já existente.")
                    print(f"{original_name}: {reason}")
                    errors.append(f"{original_name}: {reason}")
                    continue
                else:
                    print(f"{original_name}: Arquivo já existe, mas será indexado.")

            text = extrair_texto_pdf(str(file_path))
            texto_limpo = limpar_texto(text)
            linhas = texto_limpo.splitlines()

            local_file_json = Path(f"data/json/raw{file_name_unique}.json")
            local_file_json.parent.mkdir(parents=True, exist_ok=True)

            with open(local_file_json, "w", encoding="utf-8") as f:
                json.dump(linhas, f, ensure_ascii=False, indent=4)

            indexar_textos(linhas)
            redis_conn.set("recarregar_indice", "true")
            mark_as_indexed(file_hash)

            print(f"{original_name}: Processado com sucesso.")
            processed.append(original_name)

        except Exception as e:
            print(f"{original_name}: Erro ao processar: {str(e)}")
            errors.append(f"{original_name}: {str(e)}")

    return {
        "status": "completed",
        "processed": processed,
        "errors": errors
    }


def save_in_db(file_path: Path, file_name_unique: str, original_name: str, content_type: str, file_hash: str) -> dict:
    
    file_db: FileModel = {
        "filename": original_name,
        "filename_hash": file_name_unique,
        "hash_algorithm": file_hash,
        "file_type": content_type,
        "file_date": datetime.now().isoformat(),
        "is_indexed": False,
        "file_location": str(file_path)
    }
    
    # Converte o dicionário em um FileModel
    file_model = FileModel(**file_db)
    return save_file_if_not_exists(file_model)

if __name__ == "__main__":
    with redis_conn:
        worker = Worker(queues=["default"], connection=redis_conn)
        worker.work()
