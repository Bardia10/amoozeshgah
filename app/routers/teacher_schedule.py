from fastapi import APIRouter, HTTPException, Depends
from app.schemas.teacher_schedule import (
    GetPublicTeacherSchedulesResponse,
    GetTeacherSchedulesResponse,
    UpdateTeacherSchedules,
    UpdateTeacherSchedulesResponse
)
from app.repository.teacher_schedule import TeacherScheduleRepository 
from app.repository.enroll import EnrollRepository 
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin, verify_admin_self_teacher, verify_jwt


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




@router.get("/{teacher_id}", response_model=GetTeacherSchedulesResponse)
async def read_items(
    teacher_id: int,  # This is the path parameter
    db=Depends(get_db),
    user=Depends(verify_admin_self_teacher)
):
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



@router.get("/{teacher_id}", response_model=GetTeacherSchedulesResponse)
async def read_items(
    teacher_id: int,  # This is the path parameter
    db=Depends(get_db),
    user=Depends(verify_admin_self_teacher)
):
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



@router.put("/{teacher_id}", dependencies=[Depends(verify_jwt)], response_model=UpdateTeacherSchedulesResponse)
async def update_sched(body: UpdateTeacherSchedules,teacher_id: int,db=Depends(get_db),user=Depends(verify_admin_self_teacher)):
    try:
        teacher_schedule_repo = TeacherScheduleRepository(db)
        await teacher_schedule_repo.insert_many(body.busy)
        await teacher_schedule_repo.delete_many(body.free)


        return UpdateTeacherSchedulesResponse(
            message="schedules updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

