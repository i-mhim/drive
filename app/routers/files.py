from fastapi import APIRouter, status, HTTPException, Response, Depends, UploadFile, File
from .. import schemas, models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter(prefix="/files", tags =['Files'])

UPLOAD_DIR = "uploads"

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model = schemas.FileResponse)
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = f"{UPLOAD_DIR}/{utils.generate_storage_filename(file.filename)}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)
    new_file = models.File(
        filename = file.filename, 
        storage_path = file_path,
        size = file_size,
        mimetype = file.content_type,
        owner_id = current_user.id
        )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file

@router.get("/", status_code=status.HTTP_200_OK, 
response_model= list[schemas.FileResponse])
def get_files(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    files = db.query(models.File).filter(models.File.owner_id == current_user.id).all()

    return files

@router.get("/{id}", response_model=schemas.FileResponse)
def get_file(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file = db.query(models.File).filter(models.File.id == id, models.File.owner_id == current_user.id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"file with id: {id} was not found")
    return file

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file_query = db.query(models.File).filter( models.File.id == id)
    file = file_query.first()

    if file == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file with id: {id} doesnt exist")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    file_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schemas.FileResponse)
def update_file(id: int, updated_file: schemas.FileUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file_query = db.query(models.File).filter(models.File.id == id)

    file = file_query.first()

    if file == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file with id: {id} does not exist")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    file_query.update(updated_file.dict(), synchronize_session= False)

    db.commit()

    return file_query.first()

@router.get("/{id}/download", status_code=status.HTTP_200_OK)
def download_file(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    file = db.query(models.File).filter(models.File.id == id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return FileResponse(
        path=file.storage_path,
        filename=file.filename
    )