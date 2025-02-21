import datetime
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from passlib.context import CryptContext
from jose import jwt, JWTError

# AUTH CONFIGURATION
SECRET_KEY = "kilideserry"  # Replace with your actual secret key
ALGORITHM = "HS256"

# Password context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=200000)

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to verify JWT
def verify_jwt(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1] if " " in authorization else authorization
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload
    except JWTError as e:  # Capture the JWTError as 'e'
        raise HTTPException(status_code=401, detail=f"Invalid token or token has expired: {str(e)}") 

# Function to generate JWT
def generate_jwt(sub, role, days):
    payload = {
        "sub": str(sub),
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=days)  # Token expires in specified days
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token