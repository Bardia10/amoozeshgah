from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.models.auth import UserLoginResponse,UserLogin
from app.dependencies.db_dependencies import get_db
from app.dependencies.common import limiter
from app.auth.auth import hash_password,verify_password,generate_jwt
from datetime import datetime,timedelta,time, date

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
@limiter.limit("5/minute")  # Limit to 5 login attempts per minute
async def login(request: Request,user: UserLogin,db=Depends(get_db)):  
    try:
        # Fetch the user from the database
        existing_user = await db.fetchrow("SELECT * FROM users WHERE username = $1", user.username)
        
        if existing_user is None or not verify_password(user.password, existing_user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid username or password")


        token = generate_jwt(existing_user['id'],existing_user['role'],4)
        
        await db.execute(
            "INSERT INTO tokens (user_id, token) VALUES ($1, $2)",
            existing_user['id'],
            token
        )

        return UserLoginResponse(
            message="Login successful",
            token=token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
