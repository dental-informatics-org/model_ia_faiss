from db.mongo_worker import db
from db_model.file import FileModel

def save_file_if_not_exists(file: FileModel) -> dict:
    existing = db["files"].find_one({"hash_algorithm": file.hash_algorithm})
    if existing:
        file_obj = FileModel(**existing)
        return {
            "status": "skipped",
            "reason": "Arquivo já indexado." if file_obj.is_indexed else "Arquivo já existe, mas não foi indexado.",
            "data": file_obj
        }

    result = db["files"].insert_one(file.model_dump())
    return {
        "status": "inserted",
        "data": {**file.model_dump(), "_id": str(result.inserted_id)}
    }

def mark_as_indexed(hash_algorithm: str) -> None:
    db["files"].update_one(
        {"hash_algorithm": hash_algorithm},
        {"$set": {"is_indexed": True}}
    )