from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.repository.user import UserRepository 
from app.repository.token import TokenRepository 
from app.models.auth import UserLoginResponse,UserLogin
from app.dependencies.db import get_db
from app.dependencies.common import limiter
from app.auth.auth import hash_password,verify_password,generate_jwt
from datetime import datetime,timedelta,time, date

router = APIRouter()
user_repo = UserRepository()
token_repo = TokenRepository()

@router.post("/login", response_model=UserLoginResponse)
@limiter.limit("5/minute")  # Limit to 5 login attempts per minute
async def login(request: Request,user: UserLogin,db=Depends(get_db)):  
    try:
        # Fetch the user from the database
        existing_user = await user_repo.get_by_column(db, "username",user.username)
        
        if existing_user is None or not verify_password(user.password, existing_user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid username or password")


        token_record = generate_jwt(existing_user['id'],existing_user['role'])

        await token_repo.create(db, token_record)

        return UserLoginResponse(
            message="Login successful",
            token=token_record.token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
