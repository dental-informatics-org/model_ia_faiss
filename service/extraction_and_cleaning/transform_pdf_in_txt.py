import os
import fitz 
from fastapi import UploadFile

async def extrair_texto_pdf(file: UploadFile, fileNameUnique: str) -> str:
    text = ""
    try:
        file_location = os.path.join('data/pdf/', f"{fileNameUnique}.{file.content_type.split('/')[1]}")

        with open(file_location, "wb") as f:
            f.write(await file.read())

        documento = fitz.open(file_location)
        for pagina in documento:
            text += pagina.get_text()

        documento.close()
        return text
    
    except Exception as e:
        print(f"Erro ao processar {file_location}: {e}")