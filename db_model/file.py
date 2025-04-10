from pydantic import BaseModel
from bson import ObjectId

class FileModel(BaseModel):
    filename: str
    filename_hash: str
    hash_algorithm: str
    is_indexed: bool
    file_type: str
    file_date: str
    file_location: str

    class Config:
        # Usado para converter ObjectId em str
        json_encoders = {
            ObjectId: str
        }