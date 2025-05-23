from fastapi import APIRouter, HTTPException, Depends
from app.schemas.instrument import (
    InstrumentCreate,
    GetInstrumentsResponse,
    GetInstrumentResponse,
    PostInstrumentResponse,
    DeleteInstrumentResponse,
    InstrumentUpdate,  
    UpdateInstrumentResponse
)
from app.repository.instrument import InstrumentRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/instruments")

@router.get("/", response_model=GetInstrumentsResponse)
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetInstrumentsResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetInstrumentResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetInstrumentResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostInstrumentResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: InstrumentCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostInstrumentResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteInstrumentResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteInstrumentResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.put("/{item_id}", response_model=UpdateInstrumentResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: InstrumentUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateInstrumentResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_parent/{family_id}", response_model=GetInstrumentsResponse)
async def read_items(family_id: int,db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_by_parent(family_id)
        return GetInstrumentsResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))