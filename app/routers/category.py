from fastapi import APIRouter, HTTPException, Depends
from app.models.category import Category,GetCategoryResponse,GetCategoriesResponse,PostCategoryResponse
from app.repository.category import CategoryRepository
from app.dependencies.db import get_db


router = APIRouter()
item_repo = CategoryRepository()

@router.get("/categories/" ,response_model=GetCategoriesResponse)
async def read_items(db=Depends(get_db)):
    try:
        records = await item_repo.get_all(db)
        return GetCategoriesResponse(
                items=[dict(record.items()) for record in records]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.get("/categories/{item_id}",response_model=GetCategoryResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        record = await item_repo.get_by_id(db, item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetCategoryResponse(
                item= dict(record.items())
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/categories/",response_model=PostCategoryResponse)
async def create_item(item: Category, db=Depends(get_db)):
    try:
        response = await item_repo.create(db, item)
        return PostCategoryResponse(
                id=response.id,
                message="item added successfully"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/categories/{item_id}/", response_model=PostCategoryResponse)
async def delete_item(item_id: int, db= Depends(get_db)):
    try:
        # Specify the table name, in this case, it's 'categories'
        table_name = "categories"

        # Call the delete method from the repository
        result = await item_repo.delete_by_id(db, item_id)

        if result:
            return PostCategoryResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))