import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URL de conexão com o MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()  # Isso retorna o banco de dados configurado no MONGO_URI
