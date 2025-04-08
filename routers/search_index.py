from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.embeddings_and_index.embeddings_and_index import buscar_textos

router = APIRouter(prefix="/search-index", tags=["Search Index"])

class SearchRequest(BaseModel):
    consulta: str
    top_k: int = 5

@router.post("/")
async def search_texts(request: SearchRequest):
    """
    Busca textos no índice FAISS com base em uma consulta.
    """
    try:
        resultados = buscar_textos(request.consulta, request.top_k)
        return {"resultados": resultados}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))