from fastapi import FastAPI
from fastapi.responses import Response
from routers import process_file, search_index, tasks_route
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import mongo_fastapi
from service.create_index import verificar_e_criar_indices


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verifica se a conexão está funcionando
    try:
        # Verifica a conexão com o MongoDB
        await mongo_fastapi.db.command("ping")
        verificar_e_criar_indices()
        yield  # Isso garante que a aplicação continue rodando após a verificação
    except Exception as e:
        print("Erro durante a inicialização:", e)
        yield  # Aqui a aplicação pode ainda continuar, mas você pode colocar lógica para interromper se necessário

app = FastAPI(lifespan=lifespan)

# Incluindo os roteadores
app.include_router(process_file.router)
app.include_router(search_index.router)
app.include_router(tasks_route.router)

# Ignorar favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)  # Responde sem erro

# Rota inicial
@app.get("/")
def read_root():
    return {"message": "API está rodando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
