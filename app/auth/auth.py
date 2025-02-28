from fastapi import Depends, HTTPException, Request, Header,APIRouter,status
import datetime
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.dependencies.db_dependencies import get_db
from app.models.tables import Token
from app.repositories.token import TokenRepository 
from app.repositories.user import UserRepository 


# AUTH CONFIGURATION
SECRET_KEY = "kilideserry"  # Replace with your actual secret key
ALGORITHM = "HS256"


user_repo = UserRepository()
token_repo = TokenRepository()


# Password context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=200000)

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to verify JWT
async def verify_jwt(authorization: str = Header(...), db=Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1] if " " in authorization else authorization
    
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     return payload  # Return the decoded payload
    # except JWTError as e:  # Capture the JWTError as 'e'
    #     raise HTTPException(status_code=401, detail=f"Invalid token or token has expired: {str(e)}") 

    # token_entry = await db.fetchrow("SELECT user_id FROM tokens WHERE token = $1", token)
    token_entry = await token_repo.get_by_column(db, "token",token)
    
    if token_entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # user = await db.fetchrow("SELECT id,role FROM users WHERE id = $1", token_entry["user_id"])
    user = await user_repo.get_by_id(db, token_entry["user_id"])
    
    return user

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