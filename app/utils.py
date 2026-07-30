from passlib.context import CryptContext
import uuid
from pathlib import Path

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def hash(password: str):
    print("PASSWORD:", password)
    print("LENGTH:", len(password.encode("utf-8")))
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_storage_filename(filename: str) -> str:
    extension = Path(filename).suffix

    unique_name = f"{uuid.uuid4()}{extension}"

    return unique_name

def file_iterator(path):
    with open(path, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk