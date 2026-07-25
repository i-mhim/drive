from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class FileResponse(BaseModel):
    id: int
    filename: str
    storage_path: str
    size: int
    mimetype: str
    created_at: datetime

    class Config:
        from_attributes = True
