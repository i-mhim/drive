from fastapi import APIRouter, HTTPException, status, Depends, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/permissions", tags =['Permissions'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PermissionOut)
def create_permission(permission: schemas.PermissionCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    file = db.query(models.File).filter(
    models.File.id == permission.file_id,
    models.File.owner_id == current_user.id
    ).first()

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to share this file"
        )
    
    existing = db.query(models.Permission).filter(
    models.Permission.file_id == permission.file_id,
    models.Permission.user_id == permission.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already has permission"
        )
    new_permission = models.Permission(
    file_id = permission.file_id,
    folder_id = permission.folder_id,
    user_id = permission.user_id,
    role = permission.role                            
    )

    if permission.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot give permission to yourself"
    )

    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return new_permission

@router.get("/given", response_model=List[schemas.PermissionOut])
def get_permissions_given(
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):

    permissions = db.query(models.Permission).outerjoin(
        models.File,
        models.Permission.file_id == models.File.id
    ).outerjoin(
        models.Folder,
        models.Permission.folder_id == models.Folder.id
    ).filter(
        (models.File.owner_id == current_user.id) | (models.Folder.owner_id == current_user.id)
    ).all()

    return permissions

@router.get("/received", response_model=List[schemas.PermissionOut])
def get_permissions_given(
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):

    permissions = db.query(models.Permission).filter(
       models.Permission.user_id == current_user.id
    ).all()

    return permissions

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= List[schemas.PermissionOut])
def get_permissions(id: int,current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    file = db.query(models.File).filter(
    models.File.id == id,
    models.File.owner_id == current_user.id
    ).first()

    if file is None:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    permission = db.query(models.Permission).filter(models.Permission.file_id == id).all()

    return permission

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    permission_query = db.query(models.Permission).filter( models.Permission.id == id)
    permission = permission_query.first()

    if permission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"permission with id: {id} doesnt exist")
    
    if permission.file_id:
        resource = db.query(models.File).filter(
            models.File.id == permission.file_id
        ).first()
    else:
        resource = db.query(models.Folder).filter(
            models.Folder.id == permission.folder_id
        ).first()

    if resource is None:
        raise HTTPException(
        status_code=404,
        detail="Resource not found"
    )

    if resource.owner_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )
    
    permission_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schemas.PermissionOut)
def update_permission(
    id: int,
    updated_permission: schemas.PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    permission = db.query(models.Permission).filter(
        models.Permission.id == id
    ).first()

    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"permission with id: {id} does not exist"
        )

    file = db.query(models.File).filter(
        models.File.id == permission.file_id
    ).first()

    if file.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )


    permission.role = updated_permission.role

    db.commit()
    db.refresh(permission)

    return permission