import secrets
import string
import hashlib

def generate_unique_filename(length: int = 16) -> str:
    # Define o conjunto de caracteres possíveis (letras maiúsculas, minúsculas e números)
    characters = string.ascii_letters + string.digits
    
    # Gera uma string aleatória de tamanho `length`
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    
    return random_string


def get_file_hash_from_path(path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(1024):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()