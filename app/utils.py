from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def hash(password: str):
    print("PASSWORD:", password)
    print("LENGTH:", len(password.encode("utf-8")))
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)