from fastapi import FastAPI
from app.controllers.general_info_controller import router as general_info_router
from app.controllers.enrollment_controller import router as enrollment_router
#uvicorn main:app --reload
app = FastAPI()

# Setup database connection
#setup_database()

# Include routers
app.include_router(general_info_router)
app.include_router(enrollment_router)