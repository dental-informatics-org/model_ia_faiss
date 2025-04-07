import secrets
import string
import hashlib
from fastapi import UploadFile

def generate_unique_filename(length: int = 16) -> str:
    # Define o conjunto de caracteres possíveis (letras maiúsculas, minúsculas e números)
    characters = string.ascii_letters + string.digits
    
    # Gera uma string aleatória de tamanho `length`
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    
    return random_string


async def get_file_hash(file: UploadFile) -> str:
    """Função para calcular o hash de um arquivo sem consumi-lo completamente"""
    hash_md5 = hashlib.md5()
    
    # Mantenha a posição do arquivo com 'seek'
    contents = await file.read(1024)  # Lê 1KB por vez
    while contents:
        hash_md5.update(contents)
        contents = await file.read(1024)  # Continua lendo em blocos de 1KB
    
    # Reposiciona o ponteiro de leitura para o início do arquivo, permitindo que ele seja lido novamente
    await file.seek(0)
    
    return hash_md5.hexdigest()