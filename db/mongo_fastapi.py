import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URL de conexão com o MongoDB
MONGO_URI = os.getenv("MONGO_URI")
print("Mongo URI em tempo de execução:", os.getenv("MONGO_URI"))
# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["ia_index"] 
