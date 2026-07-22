from fastapi import APIRouter, status, HTTPException, Response
from utils import hash_password
from .. import schemas
from pwdlib import PasswordHash


router = APIRouter(prefix="/auth", tags =['Authentication'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate):
   hashed_password = hash_password(user.password)
   #new_user = 

    