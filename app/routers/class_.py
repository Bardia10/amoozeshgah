from fastapi import APIRouter, HTTPException, Depends
from app.schemas.class_ import (
    ClassCreate,
    GetClassesResponse,
    GetClassResponse,
    PostClassResponse,
    DeleteClassResponse,
    ClassUpdate,  
    UpdateClassResponse
)
from app.repository.class_ import ClassRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/classes")

@router.get("/", response_model=GetClassesResponse)
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetClassesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetClassResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetClassResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostClassResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: ClassCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostClassResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteClassResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteClassResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=UpdateClassResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: ClassUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateClassResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_teacher/{teacher_id}", response_model=GetClassesResponse)
async def read_items(teacher_id: int,db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_by_teacher(teacher_id)
        return GetClassesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by_course/{course_id}", response_model=GetClassesResponse)
async def read_items(course_id: int,db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_by_course(course_id)
        return GetClassesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


