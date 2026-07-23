from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth", tags =['Authentication'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   hashed_password=utils.hash_password(user.password)
   user.password = hashed_password
   new_user = models.User(**user.dict())

   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user

    