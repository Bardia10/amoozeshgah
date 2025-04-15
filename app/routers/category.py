from fastapi import APIRouter, HTTPException, Depends
from app.schemas.category import (
    CategoryCreate,
    GetCategoryResponse,
    GetCategoriesResponse,
    PostCategoryResponse,
    DeleteCategoryResponse,
)
from app.repository.category import CategoryRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin


router = APIRouter(prefix="/categories")

@router.get("/", response_model=GetCategoriesResponse)
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetCategoriesResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetCategoryResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetCategoryResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostCategoryResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: CategoryCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostCategoryResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteCategoryResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteCategoryResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









# from fastapi import APIRouter, HTTPException, Depends
# from app.models.category import Category
# from app.schemas.category import CategoryCreate,GetCategoryResponse,GetCategoriesResponse,PostCategoryResponse,DeleteCategoryResponse
# from app.repository.category import CategoryRepository as ItemRepository
# from app.dependencies.db import get_db
# from app.dependencies.auth import verify_admin


# router = APIRouter(prefix="/categories")
# item_repo = ItemRepository()

# @router.get("/" ,response_model=GetCategoriesResponse)
# async def read_items(db=Depends(get_db)):
#     try:
#         records = await item_repo.get_all(db)
#         return GetCategoriesResponse(
#                 items=[dict(record.items()) for record in records]
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))    

# @router.get("/{item_id}",response_model=GetCategoryResponse)
# async def read_item(item_id: int, db=Depends(get_db)):
#     try:
#         record = await item_repo.get_by_id(db, item_id)
#         if not record:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return GetCategoryResponse(
#                 item= dict(record.items())
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))    


# @router.post("/",response_model=PostCategoryResponse, dependencies=[Depends(verify_admin)])
# async def create_item(item: CategoryCreate, db=Depends(get_db)):
#     try:
#         response = await item_repo.create(db, item)
#         return PostCategoryResponse(
#                 id=response.id,
#                 message="item added successfully"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))    

# @router.delete("/{item_id}", response_model=DeleteCategoryResponse, dependencies=[Depends(verify_admin)])
# async def delete_item(item_id: int, db= Depends(get_db)):
#     try:
#         # Call the delete method from the repository
#         result = await item_repo.delete_by_id(db, item_id)

#         if result:
#             return DeleteCategoryResponse(
#                 id=item_id,
#                 message="Item deleted successfully"
#             )
#         else:
#             raise HTTPException(status_code=404, detail="Item not found")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))