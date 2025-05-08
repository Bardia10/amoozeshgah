from fastapi import APIRouter, HTTPException, Depends
from app.schemas.session import (
    SessionCreate,
    SessionCreateResponse,
    SessionCreateInput,
    GetEnrollsSessionsResponse
)
from app.repository.session import SessionRepository 
from app.repository.enroll import EnrollRepository 
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin, verify_admin_self_teacher, verify_jwt
from app.services.jalali_services import get_jalali

router = APIRouter(prefix="/sessions")


@router.post("/", response_model=SessionCreateResponse, dependencies=[Depends(verify_admin)])
async def post_item(item: SessionCreateInput, db=Depends(get_db)):

    try:
        dates = get_jalali(item.time,item.day,item.week_delta)
        jalali_date = dates['jalali']
        date = dates['timestamp'] 
        # Insert the new item into the items table
        session_repo = SessionRepository(db)
        enroll_repo = EnrollRepository(db)
        session= SessionCreate(enroll_id=item.enroll_id , jalali_date=jalali_date, date_at = date, time=item.time , day = item.day)
        await session_repo.create(session)
        await enroll_repo.add_spent(session.enroll_id)

        return SessionCreateResponse(
            message="session added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/{enroll_id}", response_model=GetEnrollsSessionsResponse, dependencies=[Depends(verify_admin)])
async def read_items(
    enroll_id: int,  # This is the path parameter
    db=Depends(get_db)
):
    try:
        # Instantiate the repository with the connection
        session_repo = SessionRepository(db)
        sessions = await session_repo.get_by_enroll(enroll_id)
        return GetEnrollsSessionsResponse(
            sessions=[dict(item) for item in sessions]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @router.get("/{teacher_id}", response_model=GetTeacherSchedulesResponse)
# async def read_items(
#     teacher_id: int,  # This is the path parameter
#     db=Depends(get_db),
#     user=Depends(verify_admin_self_teacher)
# ):
#     try:
#         # Instantiate the repository with the connection
#         teacher_schedule_repo = TeacherScheduleRepository(db)
#         enroll_repo = EnrollRepository(db)
#         scheds = await teacher_schedule_repo.get_by_teacher(teacher_id)
#         classes = await enroll_repo.get_by_teacher(teacher_id)
#         return GetTeacherSchedulesResponse(
#             classes=[dict(item) for item in classes],
#             busy=[dict(item) for item in scheds]
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# @router.put("/{teacher_id}", dependencies=[Depends(verify_jwt)], response_model=UpdateTeacherSchedulesResponse)
# async def update_sched(body: UpdateTeacherSchedules,teacher_id: int,db=Depends(get_db),user=Depends(verify_admin_self_teacher)):
#     try:
#         teacher_schedule_repo = TeacherScheduleRepository(db)
#         await teacher_schedule_repo.insert_many(body.busy)
#         await teacher_schedule_repo.delete_many(body.free)


#         return UpdateTeacherSchedulesResponse(
#             message="schedules updated successfully"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

