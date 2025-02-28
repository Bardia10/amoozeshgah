from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User,GetUsersResponse,GetUserResponse,PostUserResponse,DeleteUserResponse
from app.repositories.user import UserRepository as ItemRepository
from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import verify_admin


router = APIRouter()
item_repo = ItemRepository()

@router.get("/users/" ,response_model=GetUsersResponse, dependencies=[Depends(verify_admin)])
async def read_items(db=Depends(get_db)):
    try:
        records = await item_repo.get_all(db)
        return GetUsersResponse(
                items=[dict(record.items()) for record in records]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.get("/users/{item_id}",response_model=GetUserResponse)
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        record = await item_repo.get_by_id(db, item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetUserResponse(
                item= dict(record.items())
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.post("/users/",response_model=PostUserResponse)
async def create_item(item: User, db=Depends(get_db)):
    try:
        response = await item_repo.create(db, item)
        return PostUserResponse(
                id=response.id,
                message="item added successfully"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/users/{item_id}/", response_model=DeleteUserResponse)
async def delete_item(item_id: int, db= Depends(get_db)):
    try:
        # Call the delete method from the repository
        result = await item_repo.delete_by_id(db, item_id)

        if result:
            return DeleteUserResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))