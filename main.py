from fastapi import FastAPI
from app.routers.category import router as category
from app.routers.family import router as family
from app.routers.instrument import router as instrument
from app.routers.course import router as course
from app.routers.class_ import router as class_
from app.routers.enroll import router as enroll
from app.routers.teacher_schedule import router as schedule
from app.routers.session import router as session
from app.routers.user import router as user
from app.routers.auth import router as auth


app = FastAPI()


app.include_router(category)
app.include_router(family)
app.include_router(instrument)
app.include_router(course)
app.include_router(class_)
app.include_router(enroll)
app.include_router(schedule)
app.include_router(session)
app.include_router(user)
app.include_router(auth)