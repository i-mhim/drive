from fastapi import APIRouter, Depends
from ..database import get_db
from .. import oauth2,schemas, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/users", tags =['Users'])


@router.get("/", response_model=List[schemas.UserOut])
def get_current_user(
    current_user: models.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)
):
    users = db.query(models.User).all()
    return users

@router.get("/me", response_model=schemas.UserOut)
def get_current_user(
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return current_user