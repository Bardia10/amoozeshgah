from fastapi import Depends, HTTPException, Header, Request, APIRouter, status
from datetime import datetime,timezone
from app.dependencies.db import get_db
from app.repository.token import TokenRepository
from app.repository.user import UserRepository


# Function to verify JWT
async def verify_jwt(auth_token: str = Header(...), db=Depends(get_db)):
    # Check if the Authorization header is missing
    if auth_token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Extract the token from the Authorization header
    token = auth_token.split(" ")[1] if " " in auth_token else auth_token
    
    # Instantiate repositories with the database connection
    token_repo = TokenRepository(db)
    user_repo = UserRepository(db)
    
    # Get the token entry from the database using the repository
    token_entry = await token_repo.get_by_column("token", token)
    
    # If the token entry does not exist, raise an unauthorized exception
    if token_entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expires_at = token_entry["expires_at"]
    if isinstance(expires_at, datetime):  # Convert datetime to Unix timestamp if necessary
        expires_at = expires_at.timestamp()
    
    # Get current time as a Unix timestamp
    current_timestamp = datetime.now(timezone.utc).timestamp()
    if expires_at < current_timestamp:
        # Delete the expired token from the database
        await token_repo.delete_by_id(token_entry["id"])
        
        # Raise an HTTP exception for expired token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the user associated with the token from the database using the repository
    user = await user_repo.get_by_id(token_entry["user_id"])
    
    # Return the user object
    return user

# Dependency to check if user is an admin
def verify_admin(user: dict = Depends(verify_jwt)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


# Dependency to check if user is an admin or is asking for themself 
def verify_admin_self_teacher(
    user_id: int, user: dict = Depends(verify_jwt)):
    if user["role"]=="admin":
        pass
    elif user["role"]=="teacher":
        if user["id"] == user_id:
            pass
        else:
            raise HTTPException(status_code=403, detail="Not enough permissons")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


# def verify_admin_self_teacher(
#     teacher_id: int, user: dict = Depends(verify_jwt)  # Ensure `verify_jwt` is executed and returns the user object
# ):
#     # Pass the resolved `user` object to `verify_admin_self`
#     return verify_admin_self_teacher_handler(user_id=teacher_id, user=user)


# Dependency to check if user is a student
def verify_student(user: dict = Depends(verify_jwt)):
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def verify_admin_self(
    user_id: int, user: dict = Depends(verify_jwt)):
    if user["role"]=="admin":
        pass
    else:
        if user["id"] == user_id:
            pass
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    return user

# def verify_admin_self(
#     user_id: int, user: dict = Depends(verify_jwt)  # Ensure `verify_jwt` is executed and returns the user object
# ):
#     # Pass the resolved `user` object to `verify_admin_self`
#     return verify_admin_self2(user_id=user_id, user=user)