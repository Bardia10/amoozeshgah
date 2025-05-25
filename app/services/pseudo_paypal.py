from datetime import datetime,time,timedelta
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


async def create_paypal(token , amount, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)

        new_paypal = Item(id=1,token=token , amount=amount ,  is_done=False, expires_at=datetime.utcnow() + timedelta(days=1)) 
        
        response = await item_repo.create(new_paypal)

        return PaypalCreateResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def check_paypal(token: str, amount: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        
        # Check if the item exists and is done
        response = await item_repo.check_done(token, amount)

        # Return True if response exists, otherwise False
        return True if response else False
    except Exception as e:
        # Handle any exceptions and raise an HTTPException with a status code and error detail
        raise HTTPException(status_code=500, detail=str(e))