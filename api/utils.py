import hashlib
import os
import magic
from fastapi import UploadFile, HTTPException

MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 52428800))  # 50MB
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def calculate_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_file_type(file_path: str) -> str:
    return magic.from_file(file_path)

async def save_upload_file(upload_file: UploadFile, destination: str):
    try:
        with open(destination, "wb") as f:
            size = 0
            while contents := await upload_file.read(1024 * 1024):
                size += len(contents)
                if size > MAX_UPLOAD_SIZE:
                    raise HTTPException(status_code=413, detail="File too large")
                f.write(contents)
    except Exception as e:
        if os.path.exists(destination):
            os.remove(destination)
        raise e
