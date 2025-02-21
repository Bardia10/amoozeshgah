from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.models.teacher import UpdateSchedules,UpdateSchedulesResponse
from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import verify_jwt
from datetime import datetime,timedelta,time, date
from typing import Optional,List


router = APIRouter()


@router.put("/schedules", dependencies=[Depends(verify_jwt)], response_model=UpdateSchedulesResponse)
async def update_sched(body: UpdateSchedules,user: dict = Depends(verify_jwt),db=Depends(get_db)):
    if user["role"]=="admin":
        pass
    elif user["role"]=="teacher":
        if user["id"] == body.teacher_id:
            pass
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


    try:
        for item in body.busy:
            await db.execute("""
        INSERT INTO teacher_schedules (teacher_id, day, time)
        VALUES ($1, $2, $3)
        ON CONFLICT (teacher_id, day, time) 
        DO UPDATE SET 
            teacher_id = EXCLUDED.teacher_id,
            day = EXCLUDED.day,
            time = EXCLUDED.time
    """, body.teacher_id, item.day, item.time)

        for item in body.free:
            await db.execute("""
        DELETE FROM teacher_schedules 
        WHERE teacher_id = $1 AND day = $2 AND time = $3
    """,  body.teacher_id, item.day, item.time)

        return UpdateSchedulesResponse(
            message="schedules updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

