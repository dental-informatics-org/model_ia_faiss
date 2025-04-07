from fastapi import APIRouter, File, UploadFile
from typing import List
from service.process_file import process_pdf

router = APIRouter(prefix="/process-pdf", tags=["Process PDF"])

ALLOWED_TYPES = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/csv"]

@router.post("/upload-pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):

    # Verificar e processar os arquivos recebidos
    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            return {"error": f"{file.filename} não é um PDF"}

    response = await process_pdf(files)
    return response

