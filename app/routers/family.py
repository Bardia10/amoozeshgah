from fastapi import APIRouter, HTTPException, Depends
from app.schemas.family import FamilyCreate,GetFamiliesResponse,GetFamilyResponse,PostFamilyResponse,DeleteFamilyResponse
from app.repository.family import CategoryRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/families")
item_repo = ItemRepository()

@router.get("/" ,response_model=GetFamiliesResponse)
async def read_items(db=Depends(get_db)):
    try:
        records = await item_repo.get_all(db)
        return GetFamiliesResponse(
                items=[dict(record.items()) for record in records]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.get("/{item_id}",response_model=GetFamilyResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        record = await item_repo.get_by_id(db, item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetFamilyResponse(
                item= dict(record.items())
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/",response_model=PostFamilyResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: FamilyCreate, db=Depends(get_db)):
    try:
        response = await item_repo.create(db, item)
        return PostFamilyResponse(
                id=response.id,
                message="item added successfully"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/{item_id}", response_model=DeleteFamilyResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db= Depends(get_db)):
    try:
        # Call the delete method from the repository
        result = await item_repo.delete_by_id(db, item_id)

        if result:
            return DeleteFamilyResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))