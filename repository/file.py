from db.mongo_worker import db
from db_model.file import FileModel

def save_file_if_not_exists(file: FileModel) -> dict:
    existing = db["files"].find_one({"filename_hash": file.filename_hash})
    if existing:
        return {
            "status": "skipped",
            "reason": "Arquivo já indexado.",
            "data": FileModel(**existing)
        }

    result = db["files"].insert_one(file.model_dump())
    return {
        "status": "inserted",
        "data": {**file.model_dump(), "_id": str(result.inserted_id)}
    }