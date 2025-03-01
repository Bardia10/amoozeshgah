from fastapi import APIRouter, HTTPException, Depends
from app.models.item import Item,GetItemResponse,GetItemsResponse,PostItemResponse
from app.repository.item import ItemRepository
from app.dependencies.db import get_db


router = APIRouter()
item_repo = ItemRepository()

@router.get("/items/" ,response_model=GetItemsResponse)
async def read_items(db=Depends(get_db)):
    try:
        records = await item_repo.get_all(db)
        return GetItemsResponse(
                items=[dict(record.items()) for record in records]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.get("/items/{item_id}",response_model=GetItemResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        record = await item_repo.get_by_id(db, item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetItemResponse(
                item= dict(record.items())
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/items/",response_model=PostItemResponse)
async def create_item(item: Item, db=Depends(get_db)):
    try:
        response = await item_repo.create(db, item)
        return PostItemResponse(
                id=response.id,
                message="item added successfully"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
