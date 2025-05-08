
from fastapi import FastAPI, Depends, HTTPException, Request, Header
import asyncpg
from jose import jwt, JWTError
import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from datetime import datetime,timedelta,time, date
from pydantic import BaseModel, constr, conint
from enum import Enum
from typing import Optional,List




app = FastAPI()



class Day(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"

# class Enro(BaseModel):
#     firstname: constr(min_length=1, max_length=50)
#     lastname: constr(min_length=1, max_length=50)
#     ssn: constr(regex=r'^\d{3}-\d{2}-\d{4}$')  # Format: XXX-XX-XXXX
#     phone: constr(regex=r'^\+?1?\d{9,15}$')  # Phone number format
#     birth_year: conint(ge=1900, le=2023)  # Year between 1900 and 2023
#     bio: str = "I am"
#     class_id: int
#     date_of_birth: date  # YYYY-MM-DD format
#     schedule: Sched  # Nested model
#     op_day: Optional[Day] = None 

###AUTH###




###GENERAL###

# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    message: str
    token: str

# Pydantic model for user registration
class User(BaseModel):
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=1, max_length=20)


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



###ADMIN###
class CategoryCreate(BaseModel):
    title: str
    desc: str = "fr"
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s

class CategoryCreateResponse(BaseModel):
    message: str


class FamilyCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    cat_id: int

class FamilyCreateResponse(BaseModel):
    message: str


class InstrumentCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    fam_id: int

class InstrumentCreateResponse(BaseModel):
    message: str

class CourseCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    fam_id: int
    inst_id: int

class CourseCreateResponse(BaseModel):
    message: str

class ClassCreate(BaseModel):
    desc: str 
    price: conint(ge=71, le=1500) = 700
    course_id: int
    teacher_id: int

class ClassCreateResponse(BaseModel):
    message: str

class TeacherCreate(BaseModel):
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=1, max_length=20)

class TeacherCreateResponse(BaseModel):
    message: str

class SessionCreate(BaseModel):
    enroll_id: str 
    year: conint(ge=1402, le=1500)
    month: conint(ge=0, le=12)
    day: conint(ge=0, le=31)
    
class SessionCreateResponse(BaseModel):
    message: str


class ClassEnrollment(BaseModel):
    time: str
    day: str  

class AddEnrollResponse(BaseModel):
    message: str

class Schedule(BaseModel): 
    teacher_id: int
    time: str
    day: str       

class GetSchedulesResponse(BaseModel):
    classes: List[ClassEnrollment]
    busy: List[Schedule]

###STUDENT###

class EnrollCreate(BaseModel):
    firstname:str
    lastname:str
    ssn:str 
    phone:str = "09"
    birth_year:int =13
    bio:str ="i am"
    class_id:int 
    day:str
    time:str

class EnrollResponse(BaseModel):
    message: str
    url: str

class verifyPayment(BaseModel):
    token:str
    amount:int 

class verifyPaymentResponse(BaseModel):
    message: str


class Schedule(BaseModel):
    day:str
    time:str


###TEACHER###
class UpdateSchedules(BaseModel):
    teacher_id:int
    busy: List[Schedule]
    free: List[Schedule]

class UpdateSchedulesResponse(BaseModel):
    message: str

class ClassEnrollment(BaseModel):
    time: str
    day: str  
    lastname: str  
    title: str  

class Schedule(BaseModel): 
    time: str
    day: str       

class GetSchedulesResponse(BaseModel):
    classes: List[ClassEnrollment]
    busy: List[Schedule]



###DATABASE###

DATABASE_URL = "postgresql://postgres:bardiapostgres@127.0.0.1:5432/postgres"

# Function to connect to the database
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)



###AUTH###

SECRET_KEY = "kilideserry"  # Replace with your actual secret key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=200000)

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def verify_jwt(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1] if " " in authorization else authorization
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload
    except JWTError as e:  # Capture the JWTError as 'e'
        raise HTTPException(status_code=401, detail=f"Invalid token or token has expired: {str(e)}") 

def generate_jwt(sub,role,days):
    payload = {
            "sub": str(sub),
            "role": role,
            "exp": datetime.utcnow() + timedelta(days=days)  # Token expires in 30 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token



###DEPENDENCIES###
# Dependency to check if user is an admin
def verify_admin(user: dict = Depends(verify_jwt)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def verify_student(user: dict = Depends(verify_jwt)):
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

limiter = Limiter(key_func=get_remote_address)



###ADMIN###

#SIGN UP STUDENTS AND TEACHERS

@app.post("/category", dependencies=[Depends(verify_admin)], response_model=CategoryCreateResponse)
async def add_instcat(item: CategoryCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO instcategories (title, description,image) VALUES ($1, $2,$3)",
            item.title,
            item.desc,
            item.image
        )

        return CategoryCreateResponse(
            message="Item added successfully"
        )
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.post("/family", dependencies=[Depends(verify_admin)], response_model=FamilyCreateResponse)
async def add_instcat(item: FamilyCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO instfamilies (title, description,image,category_id) VALUES ($1, $2,$3,$4)",
            item.title,
            item.desc,
            item.image,
            item.cat_id
        )

        return FamilyCreateResponse(
            message="Item added successfully"
        )
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/instrument", dependencies=[Depends(verify_admin)], response_model=InstrumentCreateResponse)
async def add_course(item: InstrumentCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO instruments (title, description,image,family_id) VALUES ($1, $2,$3,$4)",
            item.title,
            item.desc,
            item.image,
            item.fam_id
        )
        return InstrumentCreateResponse(
            message="instrument added successfully"
        )
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/course", dependencies=[Depends(verify_admin)], response_model=CourseCreateResponse)
async def add_course(item: CourseCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO courses (title, description,image,family_id,instrument_id) VALUES ($1, $2,$3,$4,$5)",
            item.title,
            item.desc,
            item.image,
            item.fam_id,
            item.inst_id
        )
        return CourseCreateResponse(
            message="course added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.post("/class", dependencies=[Depends(verify_admin)], response_model=ClassCreateResponse)
async def add_class(item: ClassCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO classes (description,price,course_id,teacher_id) VALUES ($1, $2,$3,$4)",
            item.desc,
            item.price,
            item.course_id,
            item.teacher_id
        )
        return ClassCreateResponse(
            message="class added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.post("/teacher", dependencies=[Depends(verify_admin)], response_model=TeacherCreateResponse)
async def add_teacher(user: TeacherCreate):
    conn = await get_db_connection()
    try:
        # Check if the username already exists
        existing_user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password before storing it
        hashed_password = hash_password(user.password)

        # Insert the new user into the database
        await conn.execute("INSERT INTO users (username, password_hash, role) VALUES ($1, $2, $3)",
                           user.username, hashed_password, "teacher")

        return TeacherCreateResponse(
            message="teacher added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


def get_jalali(time,day,week_delta):
    # Get today's time, like give me the timestamp of today when the clock is 13:44
    now = datetime.now()
    today_time = now.replace(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]), second=0, microsecond=0)

    # Get today's day, like is it Tuesday or what, then convert it to a number when Saturday is 1 and Friday is 7
    today_day = (now.weekday() + 2) % 7 + 1  # Adjust to make Saturday = 1 and Friday = 7

    # Timestamp + day delta to get this week day time
    target_day_timestamp = today_time + timedelta(days=(day - today_day))

    # Timestamp + delta week to get the actual timestamp
    final_timestamp = target_day_timestamp + timedelta(weeks=week_delta)

    # Convert to Jalali date
    jalali_date = JalaliDate(final_timestamp)

    # Format the Jalali date as yyyy/mm/dd
    formatted_jalali_date = f"{jalali_date.year}/{jalali_date.month:02}/{jalali_date.day:02}"
    return {"date":formatted_jalali_date,"date_at":final_timestamp}

@app.post("/session", dependencies=[Depends(verify_admin)], response_model=SessionCreateResponse)
async def add_session(item: SessionCreate):
    conn = await get_db_connection()
    try:
        date = get_jalali(item.time,item.day,item.week_delta) 
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO classe_sessions (enroll_id,jalili_date,date,is_deleted) VALUES ($1, $2,$3,$4)",
            item.enroll_id,
            date,
            date_at,
            False
        )
        return TeacherCreateResponse(
            message="session added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()








# Signup route
@app.post("/add_enroll", dependencies=[Depends(verify_admin)], response_model=AddEnrollResponse)
async def add_enroll(item: EnrollCreate):
    conn = await get_db_connection()
    username=item.ssn
    password=str(item.birth_year)
    hashed_password = hash_password(password)
    
    try:
        # # Check if the username already exists
        # existing_user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", user.username)
        # if existing_user:
        #     raise HTTPException(status_code=400, detail="Username already exists")
     
        result = await conn.fetchrow("""
            INSERT INTO users (username, password_hash, role, firstname, lastname, bio, contact, ssn, year_born)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (username) 
            DO UPDATE SET 
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            contact = EXCLUDED.contact,
            bio = EXCLUDED.bio,
            year_born = EXCLUDED.year_born,
            password_hash = EXCLUDED.password_hash
            RETURNING id
        """, username, hashed_password, "student", item.firstname, item.lastname, item.bio, item.phone, item.ssn, item.birth_year)


        new_id = result["id"]
        # Insert the new item into the items table
        enroll_result = await conn.fetchrow(
            "INSERT INTO enrolls (student_id, class_id,day,time,date_at,status,credit,credit_spent) VALUES ($1, $2,$3,$4,$5,$6,$7,$8) RETURNING id",
            new_id,
            item.class_id,
            item.day,
            item.time,
            datetime.utcnow(),
            1,
            4,
            0
        )

        return AddEnrollResponse(
            message="enroll added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500,  detail=str(e))
    finally:
          await conn.close()



###GENERAL###

 
@app.get("/categories", response_model=List[Category])
async def get_instcategories():
    conn = await get_db_connection()
    try:
        items = await conn.fetch("SELECT * FROM public.instcategories")
        return [Category(**dict(item)) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.get("/families", response_model=List[Family])
async def get_items():
    conn = await get_db_connection()
    try:
        # Fetch all items from the items table
        items = await conn.fetch("SELECT * FROM instfamilies")
        return [Family(**dict(item)) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.get("/family/{fam_id}", response_model=GetFamilyResponse)
async def get_items(fam_id:int):
    conn = await get_db_connection
    try:
        # Fetch all items from the courses table
        items = await conn.fetch("SELECT * FROM courses WHERE family_id = $1", fam_id)
        
        # Fetch the description from the instfamilies table
        family = await conn.fetchrow("SELECT title,description FROM instfamilies WHERE id = $1",fam_id)

        return GetFamilyResponse(
            courses=[Course(**dict(item)) for item in items],
            title=family["title"] if family else None,
            description=family["description"] if family else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.get("/course", response_model=CourseResponse)
async def get_items(course_id: int):  # Directly use course_id as a parameter
    conn = await get_db_connection()
    try:
        # Fetch course details
        course = await conn.fetchrow("SELECT * FROM courses WHERE id = $1", course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        instrument = await conn.fetchrow("SELECT * FROM instruments WHERE id = $1", course["instrument_id"])
        classes = await conn.fetch("SELECT * FROM classes WHERE course_id = $1", course_id)
        
        class_list = []
        for class_ in classes:
            teacher = await conn.fetchrow("SELECT id, firstname, lastname, bio, image FROM users WHERE id = $1", class_["teacher_id"])
            class_list.append(ClassDetail(
                class_=Class(**dict(class_)), 
                teacher=Teacher(**dict(teacher)) if teacher else None
            ))

        return CourseResponse(
            classes=class_list,
            course=Course(**dict(course)) if course else None,
            instrument=Instrument(**dict(instrument)) if instrument else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.get("/general-schedules/{teacher_id}", response_model=GeneralSchedulesResponse)
async def get_items(teacher_id: int):
    conn = await get_db_connection()
    try:
        scheds = await conn.fetch("SELECT time,day FROM teacher_schedules WHERE teacher_id = $1", teacher_id)
        class_list = await conn.fetch("SELECT enrolls.time, enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1", teacher_id)

        return GeneralSchedulesResponse(
            classes=[EnrollmentTime(**dict(item)) for item in class_list],
            busy=[Schedule(**dict(item)) for item in scheds]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

# Login route with rate limiting
@app.post("/login", response_model=UserLoginResponse)
@limiter.limit("5/minute")  # Limit to 5 login attempts per minute
async def login(request: Request,user: UserLogin):  # Add request parameter
    conn = await get_db_connection()
    try:
        # Fetch the user from the database
        existing_user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", user.username)
        
        if existing_user is None or not verify_password(user.password, existing_user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # # Generate a JWT token
        # payload = {
        #     "username": user.username,
        #     "role": existing_user['role'],
        #     "exp": datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        token = generate_jwt(existing_user['id'],existing_user['role'],4)


        return UserLoginResponse(
            message="Login successful",
            token=token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


###########################################################

###STUDENT###





merchant_id	= "mervh123"

def request_payment(amount:int):
    callback_url = "google.com"
    token = merchant_id+callback_url+str(amount)
    return token

def create_pay_url(token:str):
    url = "google.com/"+token
    return url

@app.post("/enroll", response_model=EnrollResponse)
async def submit_enroll(item: EnrollCreate):
    conn = await get_db_connection()
    username=item.ssn
    password=str(item.birth_year)
    hashed_password = hash_password(password)
    
    try:
        result = await conn.fetchrow("""
            INSERT INTO users (username, password_hash, role, firstname, lastname, bio, contact, ssn, year_born)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (username) 
            DO UPDATE SET 
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            contact = EXCLUDED.contact,
            bio = EXCLUDED.bio,
            year_born = EXCLUDED.year_born,
            password_hash = EXCLUDED.password_hash
            RETURNING id
        """, username, hashed_password, "student", item.firstname, item.lastname, item.bio, item.phone, item.ssn, item.birth_year)

        new_id = result["id"]
        # Insert the new item into the items table
        enroll_result = await conn.fetchrow(
            "INSERT INTO enrolls (student_id, class_id,day,time,date_at,status,credit,credit_spent) VALUES ($1, $2,$3,$4,$5,$6,$7,$8) RETURNING id",
            new_id,
            item.class_id,
            item.day,
            item.time,
            datetime.utcnow(),
            0,
            4,
            0
        )
        enroll_id = enroll_result["id"]
        amount = await conn.fetchrow("SELECT price FROM classes WHERE id = $1", item.class_id)
        token=request_payment(amount["price"])
        url = create_pay_url(token)
        await conn.execute(
            "INSERT INTO pay_tokens (token,enroll_id, created_at,is_deleted) VALUES ($1, $2,$3,$4)",
            token,
            enroll_id,
            datetime.utcnow(),
            False
        )

        return EnrollResponse(
            message="enrolled successfully",
            url=url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


def verify_request(token, amount):
  return True

@app.get("/verify_payment", response_model=verifyPaymentResponse)
async def verify_payment(token: str , amount: int ):
    conn = await get_db_connection()
    try:
        pay_request = await conn.fetchrow("SELECT * FROM pay_tokens WHERE token = $1", token)
        
        # Check if the payment token exists
        if not pay_request:
            raise HTTPException(status_code=400, detail="Invalid or expired token.")

        # Verify the payment
        answer = verify_request(token=token, amount=amount)
        
        # Check if the payment was successful
        if not answer:
            raise HTTPException(status_code=400, detail="Payment has not taken place.")

        # Update the enrolls table
        await conn.execute(
            "UPDATE enrolls SET status = 1 WHERE id = $1",
            pay_request["enroll_id"]
        )

        # Update the pay_tokens table
        await conn.execute(
            "UPDATE pay_tokens SET is_deleted = TRUE, deleted_at = $1 WHERE id = $2",
            datetime.utcnow(),
            pay_request["id"]
        )

        return EnrollResponse(
            message="Payment verified successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await conn.close()



######################################################


###TEACHER###

@app.put("/schedules", dependencies=[Depends(verify_jwt)], response_model=UpdateSchedulesResponse)
async def update_sched(body: UpdateSchedules,user: dict = Depends(verify_jwt)):
    if user["role"]=="admin":
        pass
    elif user["role"]=="teacher":
        if user["sub"] == body.teacher_id:
            pass
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


    conn = await get_db_connection()
    try:
        for item in body.busy:
            await conn.execute("""
        INSERT INTO teacher_schedules (teacher_id, day, time)
        VALUES ($1, $2, $3)
        ON CONFLICT (teacher_id, day, time) 
        DO UPDATE SET 
            teacher_id = EXCLUDED.teacher_id,
            day = EXCLUDED.day,
            time = EXCLUDED.time
    """, body.teacher_id, item.day, item.time)

        for item in body.free:
            await conn.execute("""
        DELETE FROM teacher_schedules 
        WHERE teacher_id = $1 AND day = $2 AND time = $3
    """,  body.teacher_id, item.day, item.time)

        return UpdateSchedulesResponse(
            message="schedules updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.get("/schedules/{teacher_id}", dependencies=[Depends(verify_jwt)], response_model=GetSchedulesResponse)
async def get_items(teacher_id: int,user: dict = Depends(verify_jwt)):
    print(user)
    if user["role"]=="admin":
        pass
    elif user["role"]=="teacher":
        if user["sub"] == body.teacher_id:
            pass
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    
    conn = await get_db_connection()
    try:
        scheds = await conn.fetch("SELECT day,time FROM teacher_schedules WHERE teacher_id = $1", teacher_id)

        class_list = await conn.fetch("SELECT enrolls.day,enrolls.time, users.lastname,courses.title FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id INNER JOIN users ON enrolls.student_id = users.id INNER JOIN courses ON classes.course_id = courses.id WHERE classes.teacher_id = $1;", teacher_id)
        print(class_list)
        return GetSchedulesResponse(
            classes=[dict(item) for item in class_list],
            busy=[dict(item) for item in scheds]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()







# @app.post("/listest")
# async def receive_data(input_data: InputModel):
#     result_on = []
#     result_off = []

#     # Process the 'on' list
#     for item in input_data.on:
#         if item.title != "no":
#             new_title = item.title + " added"
#         else:
#             new_title = item.title  # Keep the title as is
#         result_on.append({"id": item.id, "title": new_title})

#     # Process the 'off' list
#     for item in input_data.off:
#         if item.title != "no":
#             new_title = item.title + " added"
#         else:
#             new_title = item.title  # Keep the title as is
#         result_off.append({"id": item.id, "title": new_title})

#     return {"on": result_on, "off": result_off}

###TEST###
@app.get("/")
async def read_root():
     return {"message": "Welcome to FatAPI!"}

@app.get("/items/", dependencies=[Depends(verify_jwt)])
async def read_items():
    return [{"item": "item1"}, {"item": "item2"}]

@app.post("/u")
async def add_class():
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        result=await conn.fetchrow(
            "INSERT INTO test_table (name) VALUES ('Test Name') RETURNING id;"
        )
        print("resuuuuul    ",result["id"])
        
        return {"message": "class added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()