from pydantic import BaseModel  # Importing BaseModel from pydantic

class EnrollCreate(BaseModel):
    firstname: str
    lastname: str
    ssn: str 
    phone: str = "09"
    birth_year: int = 13
    bio: str = "I am"
    class_id: int 
    day: str
    time: str

class EnrollResponse(BaseModel):
    message: str
    url: str

class VerifyPayment(BaseModel): 
    token: str
    amount: int 

class VerifyPaymentResponse(BaseModel):  
    message: str

class Schedule(BaseModel):
    day: str
    time: str