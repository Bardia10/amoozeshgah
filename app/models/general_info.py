from pydantic import BaseModel, constr, conint
from typing import Optional,List

class Category(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]


class Family(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]
    category_id: int  

class Course(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]
    family_id: int  
    instrument_id: int  

class GetFamilyResponse(BaseModel):
    courses: List[Course]
    title: str 
    description: Optional[str] = None


class Teacher(BaseModel):
    id: int
    firstname: str
    lastname: str
    bio: Optional[str] = None
    image: Optional[str] = None

class Class(BaseModel):
    id: int  
    description: Optional[str] 
    course_id: int  
    teacher_id: int 
    price: int 
    dayPerWeek: int 

class Instrument(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]
    family_id: int  
    lowPrice: int  
    midPrice: int  
    highPrice: int  

class ClassDetail(BaseModel):
    class_: Class  
    teacher: Teacher

class CourseResponse(BaseModel):
    classes: List[ClassDetail]
    course: Course
    instrument: Optional[Instrument] = None  

class EnrollmentTime(BaseModel):
    time: str
    day: str  

class Schedule(BaseModel): 
    time: str
    day: str       

class GeneralSchedulesResponse(BaseModel):
    classes: List[EnrollmentTime]
    busy: List[Schedule]