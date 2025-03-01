from fastapi import Depends, HTTPException, Header, Request,APIRouter,status
from app.dependencies.db import get_db
from app.repository.token import TokenRepository 
from app.repository.user import UserRepository 


user_repo = UserRepository()
token_repo = TokenRepository()


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