from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator
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
    folder_id: Optional[int] = None

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

class PermissionCreate(BaseModel):
    file_id: Optional[int] = None
    folder_id: Optional[int] = None
    user_id: int
    role: str
    @model_validator(mode="after")
    def check_resource(self):
        if self.file_id is None and self.folder_id is None:
            raise ValueError(
                "Either file_id or folder_id must be provided"
            )

        if self.file_id is not None and self.folder_id is not None:
            raise ValueError(
                "Only one of file_id or folder_id can be provided"
            )

        return self

class PermissionOut(BaseModel):
    id: int
    file_id: Optional[int] = None
    folder_id: Optional[int] = None
    user_id: int
    created_at: datetime
    role: str

    class Config:
        from_attributes = True

class PermissionUpdate(BaseModel):
    role: str