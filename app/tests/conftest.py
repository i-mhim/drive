from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models, utils, oauth2
import os

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(autocommit=False, autoflush= False,expire_on_commit=False, bind= engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client, session):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    user = models.User(
        email=user_data["email"],
        password=utils.hash(user_data["password"])
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "user": user,
        "password": user_data["password"]
    }

@pytest.fixture
def test_user2(client, session):
    user_data = {
        "email": "another@example.com",
        "password": "password123"
    }

    user = models.User(
        email=user_data["email"],
        password=utils.hash(user_data["password"])
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "user": user,
        "password": user_data["password"]
    }

@pytest.fixture
def authorized_client(client, test_user):
    token = oauth2.create_access_token(
        {"user_id": test_user["user"].id}
    )

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def authorized_client2(client, test_user2):
    token = oauth2.create_access_token(
        {"user_id": test_user2["user"].id}
    )

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_file(session, test_user):
    os.makedirs("uploads", exist_ok=True)

    path = "uploads/test.txt"

    with open(path, "wb") as f:
        f.write(b"Hello World")

    file = models.File(
        filename="test.txt",
        storage_path=path,
        size=os.path.getsize(path),
        mimetype="text/plain",
        owner_id=test_user["user"].id,
    )

    session.add(file)
    session.commit()
    session.refresh(file)

    return file

@pytest.fixture
def test_folder(session, test_user):
    folder = models.Folder(
        name="Documents",
        owner_id=test_user["user"].id,
        parent_folder_id=None
    )

    session.add(folder)
    session.commit()
    session.refresh(folder)

    return folder

@pytest.fixture
def test_permission(session, test_file, test_user2):
    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)

    return permission

@pytest.fixture
def test_folder_permission(session, test_folder, test_user2):
    permission = models.Permission(
        folder_id=test_folder.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)

    return permission