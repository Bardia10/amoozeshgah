from pydantic import BaseModel  


class UserLogin(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    message: str
    token: str