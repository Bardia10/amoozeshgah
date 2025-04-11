from fastapi import Depends, HTTPException, Header, Request, APIRouter, status
from app.dependencies.db import get_db
from app.repository.token import TokenRepository
from app.repository.user import UserRepository


# Function to verify JWT
async def verify_jwt(auth_token: str = Header(...), db=Depends(get_db)):
    if auth_token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_token.split(" ")[1] if " " in auth_token else auth_token
    
    # Instantiate repositories with the connection
    token_repo = TokenRepository(db)
    user_repo = UserRepository(db)
    
    # Get the token entry from the database using the repository
    token_entry = await token_repo.get_by_column("token", token)
    
    if token_entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the user associated with the token from the database using the repository
    user = await user_repo.get_by_id(token_entry["user_id"])
    
    return user

# Dependency to check if user is an admin
def verify_admin(user: dict = Depends(verify_jwt)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

# Dependency to check if user is a student
def verify_student(user: dict = Depends(verify_jwt)):
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user