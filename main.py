from fastapi import FastAPI
from app.routers.item_router import router as item_router
from app.routers.category_router import router as category_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
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


app.include_router(item_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(auth_router)