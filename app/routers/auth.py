from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, models, utils, database, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags =['Authentication'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   hashed_password=utils.hash(user.password)
   user.password = hashed_password
   new_user = models.User(**user.dict())

   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

   if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
   if not utils.verify(user_credentials.password, user.password):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
   access_token = oauth2.create_access_token(data={"user_id": user.id})
   return {"access_token": access_token, "token_type": "Bearer"}
