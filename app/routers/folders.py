from fastapi import APIRouter, status, HTTPException, Depends, Response
from app import oauth2, schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(prefix="/folders", tags =['Folders'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.FolderOut)
def create_folder(
    folder: schemas.FolderCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    if folder.parent_folder_id:
        parent_folder = db.query(models.Folder).filter(
            models.Folder.id == folder.parent_folder_id,
            models.Folder.owner_id == current_user.id
        ).first()

        if not parent_folder:
            raise HTTPException(
                status_code=404,
                detail="Parent folder not found"
            )
    
    existing = (
    db.query(models.Folder)
    .filter(
        models.Folder.parent_folder_id == folder.parent_folder_id,
        models.Folder.name == folder.name
    )
    .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Folder with this name already exists in the parent folder.")

    new_folder = models.Folder(
        name = folder.name,
        owner_id = current_user.id, parent_folder_id = folder.parent_folder_id
    )
    
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return new_folder

@router.get("/", status_code = status.HTTP_200_OK, response_model=List[schemas.FolderOut])
def get_folders(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    folder = db.query(models.Folder).filter(models.Folder.owner_id == current_user.id).all()

    return folder

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model= schemas.FolderOut)
def get_folder(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    folder_query = db.query(models.Folder).filter(models.Folder.id == id, models.Folder.owner_id == current_user.id)
    folder = folder_query.first()

    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"folder with id: {id} was not found")


    return folder

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    folder_query = db.query(models.Folder).filter( models.Folder.id == id)
    folder = folder_query.first()

    if folder == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"folder with id: {id} doesnt exist")
    
    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    folder_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schemas.FolderOut)
def update_folder(id: int, updated_file: schemas.FolderUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    folder_query = db.query(models.Folder).filter(models.Folder.id == id)

    folder = folder_query.first()

    if folder == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"folder with id: {id} does not exist")
    
    if folder.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    folder_query.update(updated_file.dict(), synchronize_session= False)

    db.commit()

    return folder_query.first()