from fastapi import APIRouter, HTTPException, Depends
from app.models.pseudo_paypal import PseudoPaypal as Item 
from app.schemas.pseudo_paypal import (
    GetPseudoPaypalResponse,
    PaypalCreateInput,
    PaypalCreateResponse,
    UpdatePseudoPaypalResponse
)
from app.repository.pseudo_paypal import PseudoPaypalRepository as ItemRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin
from datetime import datetime,time,timedelta
from app.services.pseudo_paypal import create_paypal

router = APIRouter(prefix="/pseudo_paypal")

# @router.get("/", response_model=GetCategoriesResponse)
# async def read_items(db=Depends(get_db)):
#     try:
#         # Instantiate the repository with the connection
#         item_repo = ItemRepository(db)
#         records = await item_repo.get_all()
#         return GetCategoriesResponse(
#             items=[dict(record.items()) for record in records]
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_token}", response_model=GetPseudoPaypalResponse)
async def read_item(item_token: str, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_column( "token",item_token)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetPseudoPaypalResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.put("/{item_id}", response_model=UpdatePseudoPaypalResponse)
async def update_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)

        # Perform the update operation
        result = await item_repo.edit_column(item_id, "is_done",True)

        if result:
            return UpdatePseudoPaypalResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





