from fastapi import APIRouter, HTTPException, Depends
from app.schemas.session import (
    SessionCreate,
    SessionCreateResponse,
    SessionCreateInput,
    GetEnrollsSessionsResponse,
    SessionUpdate,  
    UpdateSessionResponse
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




@router.put("/{item_id}", response_model=UpdateSessionResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: SessionUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateSessionResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))