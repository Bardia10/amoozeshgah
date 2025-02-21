from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.models.general_info import Category,Family,GetFamilyResponse,Course,CourseResponse,Teacher,Class,ClassDetail,CourseResponse,Instrument,EnrollmentTime,Schedule,GeneralSchedulesResponse
from app.database.db_dependencies import get_db
from typing import Optional,List

router = APIRouter()



@router.get("/categories", response_model=List[Category])
async def get_instcategories( db=Depends(get_db)):
    items = await db.fetch("SELECT * FROM categories")      
    return [Category(**dict(item)) for item in items]


@router.get("/families", response_model=List[Family])
async def get_items(db=Depends(get_db)):
        # Fetch all items from the items table
        items = await db.fetch("SELECT * FROM families")
        return [Family(**dict(item)) for item in items]

@router.get("/family/{fam_id}", response_model=GetFamilyResponse)
async def get_items(fam_id:int,db=Depends(get_db)):
        # Fetch all items from the courses table
        items = await db.fetch("SELECT * FROM courses WHERE family_id = $1", fam_id)
        
        # Fetch the description from the families table
        family = await db.fetchrow("SELECT title,description FROM instfamilies WHERE id = $1",fam_id)

        return GetFamilyResponse(
            courses=[Course(**dict(item)) for item in items],
            title=family["title"] if family else None,
            description=family["description"] if family else None
        )



@router.get("/course/{course_id}", response_model=CourseResponse)
async def get_items(course_id: int,db=Depends(get_db)):
        # Fetch course details
        course = await db.fetchrow("SELECT * FROM courses WHERE id = $1", course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        instrument = await db.fetchrow("SELECT * FROM instruments WHERE id = $1", course["instrument_id"])
        classes = await db.fetch("SELECT * FROM classes WHERE course_id = $1", course_id)
        
        class_list = []
        for class_ in classes:
            teacher = await db.fetchrow("SELECT id, firstname, lastname, bio, image FROM users WHERE id = $1", class_["teacher_id"])
            class_list.append(ClassDetail(
                class_=Class(**dict(class_)), 
                teacher=Teacher(**dict(teacher)) if teacher else None
            ))

        return CourseResponse(
            classes=class_list,
            course=Course(**dict(course)) if course else None,
            instrument=Instrument(**dict(instrument)) if instrument else None
        )

@router.get("/general-schedules/{teacher_id}", response_model=GeneralSchedulesResponse)
async def get_items(teacher_id: int,db=Depends(get_db)):
        scheds = await db.fetch("SELECT time,day FROM teacher_schedules WHERE teacher_id = $1", teacher_id)
        class_list = await db.fetch("SELECT enrolls.time, enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1", teacher_id)

        return GeneralSchedulesResponse(
            classes=[EnrollmentTime(**dict(item)) for item in class_list],
            busy=[Schedule(**dict(item)) for item in scheds]
        )



@router.get("/items/{item_id}", response_model=Category)
async def read_item(item_id: int, db=Depends(get_db)):
    # Query the database for the item with the given item_id
    item = await db.fetchrow("SELECT * FROM categories WHERE id = $1", item_id)
    if item is None:
            raise HTTPException(status_code=404, detail="item not found")
    return dict(item)  # Convert the record to a dictionary

@router.post("/items/")
async def create_item(item: Category, db=Depends(get_db)):
    # Logic to create an item in the database
    pass