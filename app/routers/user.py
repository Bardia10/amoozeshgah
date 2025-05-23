from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import (
    UserCreate,
    GetUsersResponse,
    GetUserResponse,
    PostUserResponse,
    DeleteUserResponse,
    UserUpdate,  
    UpdateUserResponse,
    UpdateUsersPassword,
    UpdateUsersPasswordResponse,
    GetTeachersPublicResponse
)
from app.repository.user import UserRepository as ItemRepository
from app.dependencies.db import get_db
from app.auth.auth import hash_password
from app.dependencies.auth import verify_admin, verify_admin_self, verify_jwt

# Define the prefix for all routes
router = APIRouter(prefix="/users")

@router.get("/", response_model=GetUsersResponse, dependencies=[Depends(verify_admin)])
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetUsersResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetUserResponse, dependencies=[Depends(verify_admin)])
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetUserResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostUserResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: UserCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostUserResponse(
            id=response.id,
            message="item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteUserResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteUserResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=UpdateUserResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: UserUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateUserResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/change_password/{user_id}", dependencies=[Depends(verify_jwt)], response_model=UpdateUsersPasswordResponse)
async def update_users_password(body: UpdateUsersPassword,user_id: int,db=Depends(get_db) ,user=Depends(verify_admin_self)):
    try:
        hashed_password = hash_password(body.new_password)

        user_repo = ItemRepository(db)
        await user_repo.edit_column(user_id ,'password_hash',hashed_password)

        return UpdateUsersPasswordResponse(
            message="password updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teachers/public", response_model=GetTeachersPublicResponse)
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_teachers_public()
        return GetTeachersPublicResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

