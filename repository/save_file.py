from datetime import datetime
from fastapi import UploadFile
from util.generate_string import generate_unique_filename, get_file_hash

async def save_file(file: UploadFile) -> str:
    filename = file.filename
    hash_algorithm = await get_file_hash(file)
    filename_hash= f"{generate_unique_filename()}.{file.filename.split('.')[-1]}"
    file_type = file.content_type
    file_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_location = f"dataset/{file.filename.split('.')[-1]}/{filename_hash}"
    print(f"{filename} - {hash_algorithm} - {filename_hash} - {file_type} - {file_date} - {file_location}")