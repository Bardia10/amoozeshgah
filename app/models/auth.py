from pydantic import BaseModel, constr, conint, Field


class UserLogin(BaseModel):
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=1, max_length=20)

class UserLoginResponse(BaseModel):
    message: str
    token: str