import datetime
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.dependencies.db import get_db
from app.models.token import Token
from config.settings import settings


# AUTH CONFIGURATION
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.hash_algorithm





# Password context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=200000)

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# Function to generate JWT
def generate_jwt(sub, role):
    created_at = datetime.utcnow()
    expired_at = created_at + timedelta(days=4)
    payload = {
        "sub": str(sub),
        "role": role,
        "exp": expired_at  # Token expires in specified days
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return Token(
        user_id=sub,
        token=token,
        created_at=created_at,
        expires_at=expired_at
    )