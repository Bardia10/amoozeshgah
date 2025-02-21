from fastapi import Depends, HTTPException
from app.auth.auth import verify_jwt  # Import the verify_jwt function

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