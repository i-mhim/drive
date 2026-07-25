from fileinput import filename
from fastapi import APIRouter, status, HTTPException, Response, Depends, UploadFile, File
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session
import os
import shutil

router = APIRouter(prefix="/files", tags =['Files'])

UPLOAD_DIR = "uploads"

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model = schemas.FileResponse)
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)

    new_file = models.File(
        filename = file.filename, 
        storage_path = file_path,
        size = file_size,
        mimetype = file.content_type
        )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


