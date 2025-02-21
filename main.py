from fastapi import FastAPI
from app.controllers.general_info_controller import router as item_router
# from app.database import setup_database

app = FastAPI()

# Setup database connection
#setup_database()

# Include routers
app.include_router(item_router)