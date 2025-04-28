from fastapi import APIRouter, HTTPException, Depends
from app.schemas.teacher_schedule import (
    GetPublicTeacherSchedulesResponse,
    GetTeacherSchedulesResponse
)
from app.repository.teacher_schedule import TeacherScheduleRepository 
from app.repository.enroll import EnrollRepository 
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin, verify_admin_self


router = APIRouter(prefix="/teacher_schedules")


@router.get("/public/{teacher_id}", response_model=GetPublicTeacherSchedulesResponse)
async def read_items(teacher_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        teacher_schedule_repo = TeacherScheduleRepository(db)
        enroll_repo = EnrollRepository(db)
        records = await teacher_schedule_repo.get_public_by_teacher(teacher_id)
        classes = await enroll_repo.get_public_by_teacher(teacher_id)
        records += classes
        return GetPublicTeacherSchedulesResponse(            items=[dict(record.items()) for record in records]
)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{teacher_id}", response_model=GetTeacherSchedulesResponse, dependencies=[Depends(verify_admin_self(user_id=teacher_id))])
async def read_items(teacher_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        teacher_schedule_repo = TeacherScheduleRepository(db)
        enroll_repo = EnrollRepository(db)
        scheds = await teacher_schedule_repo.get_by_teacher(teacher_id)
        classes = await enroll_repo.get_by_teacher(teacher_id)
        return GetTeacherSchedulesResponse(
            classes=[dict(item) for item in classes],
            busy=[dict(item) for item in scheds]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))