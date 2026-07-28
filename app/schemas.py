from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class FileResponse(BaseModel):
    id: int
    filename: str
    storage_path: str
    size: int
    mimetype: str
    created_at: datetime
    owner_id: int
    folder_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class FileUpdate(BaseModel):
    filename: str

class FolderCreate(BaseModel):
    name: str
    parent_folder_id: int | None = None

class FolderOut(BaseModel):
    id: int
    name: str
    owner_id: int
    parent_folder_id: Optional[int] = None

    class config: 
        from_attributes = True

class FolderUpdate(BaseModel):
    name: str