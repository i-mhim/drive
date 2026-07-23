from fastapi import FastAPI
from app.routers import auth, users, files, folders, shares, permissions
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "WOrld"}

app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(files.router)
# app.include_router(folders.router)
# app.include_router(shares.router)
# app.include_router(permissions.router)