from fastapi import FastAPI
# from app.routers.item import router as item
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
# from app.controllers.general_info_controller import router as general_info_router
# from app.controllers.enrollment_controller import router as enrollment_router
# from app.controllers.auth_controller import router as auth_router
# from app.controllers.admin_controller import router as admin_router
# from app.controllers.teacher_controller import router as teacher_router
#uvicorn main:app --reload
app = FastAPI()

# Setup database connection
#setup_database()

# # Include routers
# app.include_router(general_info_router)
# app.include_router(enrollment_router)
# app.include_router(auth_router)
# app.include_router(admin_router)
# app.include_router(teacher_router)


# app.include_router(item)
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