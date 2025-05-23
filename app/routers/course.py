from fastapi import APIRouter, HTTPException, Depends
from app.schemas.course import (
    CourseCreate,
    GetCoursesResponse,
    GetCourseResponse,
    PostCourseResponse,
    DeleteCourseResponse,
    CourseUpdate,  
    UpdateCourseResponse
)
from app.repository.course import CourseRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/courses")

@router.get("/", response_model=GetCoursesResponse)
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetCoursesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetCourseResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetCourseResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostCourseResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: CourseCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostCourseResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteCourseResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteCourseResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=UpdateCourseResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: CourseUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateCourseResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_parent/{family_id}", response_model=GetCoursesResponse)
async def read_items(family_id: int,db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_by_parent(family_id)
        return GetCoursesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))