
# from fastapi import FastAPI, Depends, HTTPException, Request
# from jose import JWTError, jwt
# import datetime

# SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
# ALGORITHM = "HS256"  # Algorithm for encoding/decoding

# app = FastAPI()

# # Dependency to check JWT
# def verify_jwt(request: Request):
#     token = request.headers.get("Authorization")
    
#     if token is None:
#         raise HTTPException(status_code=401, detail="Authorization header missing")
    
#     token = token.split(" ")[1] if " " in token else token
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload  # Return the decoded payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token or token has expired")

# # Dependency to check if user is an admin
# def verify_admin(user: dict = Depends(verify_jwt)):
#     if user.get("role") != "admin":
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return user

# # Endpoint to generate a token
# @app.get("/get-token")
# def get_token():
#     # Example payload with user ID and role
#     payload = {
#         "user_id": 123,
#         "role": "admin",  # Change to "user" for regular users
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expires in 30 minutes
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return {"token": token}

# # Endpoint to get info, requires a valid token
# @app.get("/get-info")
# async def get_info(user: dict = Depends(verify_jwt)):
#     return {"message": "This is some protected info", "user": user}

# # Endpoint to get admin info, requires admin role
# @app.get("/get-ad")
# async def get_ad(user: dict = Depends(verify_admin)):
#     return {"message": "This is admin info", "user": user}

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to FastAPI!"}


from fastapi import FastAPI, Depends, HTTPException, Request, Header
from pydantic import BaseModel
from typing import List
import asyncpg
from jose import jwt, JWTError
import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from datetime import datetime,timedelta

DATABASE_URL = "postgresql://postgres:bardiapostgres@127.0.0.1:5432/postgres"
SECRET_KEY = "kilideserry"  # Replace with your actual secret key
ALGORITHM = "HS256"

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

# Password hashing context with bcrypt and a cost factor of 10
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto", pbkdf2_sha256__rounds=200000)
# Pydantic model for user registration
class User(BaseModel):
    username: str
    password: str

# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str

class InstcatCreate(BaseModel):
    title: str
    desc: str = "fr"
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s

class InstfamCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    cat_id: int

class InstrumentCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    fam_id: int

class CourseCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    fam_id: int
    inst_id: int

class ClassCreate(BaseModel):
    desc: str 
    price: int = 700
    course_id: int
    teacher_id: int



class EnrollCreate(BaseModel):
    student_id:int
    class_id:int
    day:str
    time:str




class Sched(BaseModel):
    day:str
    time:str

class UpdateSched(BaseModel):
    teacher_id:int
    busy: List[Sched]
    free: List[Sched]


# Function to connect to the database
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Dependency to check JWT
# def verify_jwt(request: Request):
#     token = request.headers.get("Authorization")
    
#     if token is None:
#         raise HTTPException(status_code=401, detail="Authorization header missing")
    
#     token = token.split(" ")[1] if " " in token else token
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload  # Return the decoded payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token or token has expired")

def verify_jwt(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1] if " " in authorization else authorization
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload
    except JWTError as e:  # Capture the JWTError as 'e'
        raise HTTPException(status_code=401, detail=f"Invalid token or token has expired: {str(e)}") 



# Dependency to check if user is an admin
def verify_admin(user: dict = Depends(verify_jwt)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def verify_student(user: dict = Depends(verify_jwt)):
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


@app.get("/items/", dependencies=[Depends(verify_jwt)])
async def read_items():
    return [{"item": "item1"}, {"item": "item2"}]



# Signup route
@app.post("/signup")
async def signup(user: User):
    conn = await get_db_connection()
    try:
        # Check if the username already exists
        existing_user = await conn.fetchrow("SELECT * FROM users WHERE username = $1", user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password before storing it
        hashed_password = hash_password(user.password)

        # # Insert the new user into the database
        # await conn.execute("INSERT INTO users (username, password_hash, role) VALUES ($1, $2, $3)",
        #                    user.username, hashed_password, "student")
        result = await conn.execute(
       "INSERT INTO users (username, password_hash, role) VALUES ($1, $2, $3) RETURNING id",
        user.username, hashed_password, "student"
        )

        new_id = await result.fetchone()
        # # Generate a JWT token
        # payload = {
        #     "username": user.username,
        #     "role": "student",
        #     "exp": datetime.utcnow() + timedelta(days=7)  # Token expires in 30 minutes
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        token = generate_jwt(new_id,"student",4)

        return {"message": "User created successfully", "token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

# Login route with rate limiting
@app.post("/login")
@limiter.limit("5/minute")  # Limit to 5 login attempts per minute
async def login(request: Request, user: UserLogin):  # Add request parameter
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

        return {"message": "Login successful", "token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

def generate_jwt(sub,role,days):
    payload = {
            "sub": sub,
            "role": role,
            "exp": datetime.utcnow() + timedelta(days=days)  # Token expires in 30 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
 
@app.get("/get_instcat")
async def get_items(request: Request):
    conn = await get_db_connection()
    try:
        # Fetch all items from the items table
        items = await conn.fetch("SELECT * FROM public.instcategories")
        return {"items": [dict(item) for item in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.get("/instfams")
async def get_items(request: Request):
    conn = await get_db_connection()
    try:
        # Fetch all items from the items table
        items = await conn.fetch("SELECT * FROM instfamilies")
        return {"instfams": [dict(item) for item in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


        
@app.get("/instfam")
async def get_items(fam_id: int, request: Request):
    conn = await get_db_connection()
    try:
        # Fetch all items from the courses table
        items = await conn.fetch("SELECT * FROM courses WHERE family_id = $1", fam_id)
        
        # Fetch the description from the instfamilies table
        description = await conn.fetchrow("SELECT description FROM instfamilies WHERE id = $1", fam_id)

        return {
            "courses": [dict(item) for item in items],
            "description": description["description"] if description else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.get("/course")
async def get_items(course_id: int, request: Request):
    conn = await get_db_connection()
    try:
        course = await conn.fetchrow("SELECT * FROM courses WHERE id = $1", course_id)
        classes = await conn.fetch("SELECT * FROM classes WHERE course_id = $1", course_id)
        #classes has a teacher_id column based on it we want to find teachers info in users table
        class_list = []
        for class_ in classes:
          teacher = await conn.fetchrow("SELECT id , firstname, lastname , bio, image FROM users WHERE id = $1", class_["teacher_id"])
          class_list.append({"class_":class_,"teacher":teacher})
        return {
            "classes": [dict(item) for item in class_list],
            "course": course
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.get("/sched")
async def get_items(teacher_id: int, request: Request):
    conn = await get_db_connection()
    try:
        scheds = await conn.fetch("SELECT * FROM teacher_schedules WHERE teacher_id = $1", teacher_id)
        # classes = await conn.fetch("SELECT * FROM classes WHERE teacher_id = $1", teacher_id)
        # class_list = []
        # for class_ in classes:
        #   enrolls = await conn.fetch("SELECT time , day FROM enrolls WHERE class_id = $1",  class_["id"])
        #   class_list.extend(enrolls)
        class_list = await conn.fetch("SELECT enrolls.time , enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1", teacher_id)

        return {
            "classes": [dict(item) for item in class_list],
            "busy": [dict(item) for item in scheds]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.post("/add_instcat", dependencies=[Depends(verify_admin)])
async def add_instcat(item: InstcatCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO instcategories (title, description,image) VALUES ($1, $2,$3)",
            item.title,
            item.desc,
            item.image
        )
        return {"message": "Item added successfully"}
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.post("/add_instfam", dependencies=[Depends(verify_admin)])
async def add_instcat(item: InstfamCreate):
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
        return {"message": "Item added successfully"}
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/add_instrument", dependencies=[Depends(verify_admin)])
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
        return {"message": "instrument added successfully"}
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/add_course", dependencies=[Depends(verify_admin)])
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
        return {"message": "course added successfully"}
    except Exception as e:
        print("h")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.post("/enroll", dependencies=[Depends(verify_student)])
async def add_enroll(item: EnrollCreate):
    conn = await get_db_connection()
    try:
        # Insert the new item into the items table
        await conn.execute(
            "INSERT INTO enrolls (student_id, class_id,day,time,date_at) VALUES ($1, $2,$3,$4,$5)",
            item.student_id,
            item.class_id,
            item.day,
            item.time,
            datetime.utcnow()
        )
        return {"message": "enrolled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.post("/add_class", dependencies=[Depends(verify_admin)])
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
        return {"message": "class added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.post("/add_teacher", dependencies=[Depends(verify_admin)])
async def add_teacher(user: User):
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

        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@app.put("/teacher_sched", dependencies=[Depends(verify_jwt)])
async def update_sched(body: UpdateSched,user: dict = Depends(verify_jwt)):
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

        return {"message": "sched updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.get("/teacher_sched", dependencies=[Depends(verify_jwt)])
async def get_items(teacher_id: int,user: dict = Depends(verify_jwt)):
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
        scheds = await conn.fetch("SELECT * FROM teacher_schedules WHERE teacher_id = $1", teacher_id)
        # enroll_list = await conn.fetch("SELECT enrolls.time , enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1", teacher_id)
        class_list = await conn.fetch("SELECT enrolls.day,enrolls.time, users.lastname,courses.title FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id INNER JOIN users ON enrolls.student_id = users.id INNER JOIN courses ON classes.course_id = courses.id WHERE classes.teacher_id = $1;", teacher_id)
        return {
            "classes": [dict(item) for item in class_list],
            "busy": [dict(item) for item in scheds]
        }
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




@app.get("/")
async def read_root():
     return {"message": "Welcome to FatAPI!"}