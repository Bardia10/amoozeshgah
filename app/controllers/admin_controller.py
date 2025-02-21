from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.models.admin import CategoryCreate,CategoryCreateResponse
from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import verify_admin
from app.auth.auth import hash_password
from datetime import datetime,timedelta,time, date
from typing import Optional,List

router = APIRouter()


@router.post("/category", dependencies=[Depends(verify_admin)], response_model=CategoryCreateResponse)
async def add_instcat(item: CategoryCreate,db=Depends(get_db)):
    try:
        # Insert the new item into the items table
        await db.execute(
            "INSERT INTO categories (title, description,image) VALUES ($1, $2,$3)",
            item.title,
            item.desc,
            item.image
        )

        return CategoryCreateResponse(
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))