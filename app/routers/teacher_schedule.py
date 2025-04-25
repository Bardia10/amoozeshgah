from fastapi import APIRouter, HTTPException, Depends
from app.schemas.teacher_schedule import (
    GetTeacherScheduleResponse
)
from app.repository.teacher_schedule import TeacherScheduleRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/teacher_schedules")


@router.get("/public/{item_id}", response_model=GetTeacherScheduleResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_teacher(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetTeacherScheduleResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

