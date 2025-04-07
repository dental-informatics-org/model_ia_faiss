import json
from typing import List
from redis import Redis
from rq import Worker, Queue
from service.embeddings_and_index.embeddings_and_index import indexar_textos
from service.extraction_and_cleaning.clean_txt import limpar_texto

redis_conn = Redis(host="redis", port=6379)
fila = Queue(connection=redis_conn)

def process_pdf_task(files_data: List[dict]):
    errors = []
    for file_data in files_data:
        file_hash = file_data["hash"]
        file_name = file_data["filename"]
        text = file_data["text"]

        texto_limpo = limpar_texto(text)
        linhas = texto_limpo.splitlines()

        local_file_json = f"data/json/{file_name}.json"

        # Salvar como JSON
        with open(local_file_json, "w", encoding="utf-8") as f:
            json.dump(linhas, f, ensure_ascii=False, indent=4)

        indexar_textos(linhas)

    return {"status": "completed", "errors": errors}

if __name__ == "__main__":
    with redis_conn:
        worker = Worker(queues=["default"], connection=redis_conn)
        worker.work()
