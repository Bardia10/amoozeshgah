from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate
from app.schemas.pay_token import PayTokenCreate
from app.schemas.payment import PaymentCreate
from app.schemas.enroll import (
    EnrollCreate,
    EnrollSubmit,
    GetEnrollsResponse,
    GetEnrollResponse,
    PostEnrollResponse,
    SubmitEnrollResponse,
    DeleteEnrollResponse,
    VerifyEnrollResponse,
    EnrollUpdate,  
    UpdateEnrollResponse
)
from app.repository.enroll import EnrollRepository as ItemRepository
from app.repository.user import UserRepository 
from app.repository.class_ import ClassRepository 
from app.repository.pay_token import PayTokenRepository 
from app.repository.payment import PaymentRepository 
from app.repository.token import TokenRepository
from app.dependencies.db import get_db
from app.dependencies.auth import verify_admin
from app.auth.auth import hash_password, generate_jwt
from app.services.payment_services import verify_payment , request_payment , create_pay_url
from datetime import datetime,time,timedelta

router = APIRouter(prefix="/enrolls")

@router.get("/", response_model=GetEnrollsResponse, dependencies=[Depends(verify_admin)])
async def read_items(db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        records = await item_repo.get_all()
        return GetEnrollsResponse(
            items=[dict(record.items()) for record in records]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=GetEnrollResponse, dependencies=[Depends(verify_admin)])
async def read_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        record = await item_repo.get_by_id(item_id)
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return GetEnrollResponse(item=dict(record.items()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PostEnrollResponse, dependencies=[Depends(verify_admin)])
async def create_item(item: EnrollCreate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        response = await item_repo.create(item)
        return PostEnrollResponse(
            id=response.id,
            message="Item added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=DeleteEnrollResponse, dependencies=[Depends(verify_admin)])
async def delete_item(item_id: int, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        result = await item_repo.delete_by_id(item_id)

        if result:
            return DeleteEnrollResponse(
                id=item_id,
                message="Item deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit/", response_model=SubmitEnrollResponse)
async def create_item(item: EnrollSubmit, db=Depends(get_db)):
    try:
        username=str(item.ssn)
        password=str(item.ssn)
        hashed_password = hash_password(password)
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        user_repo = UserRepository(db)
        class_repo = ClassRepository(db)
        pay_token_repo = PayTokenRepository(db)
        token_repo = TokenRepository(db)

        user_info = UserCreate(username=username, password_hash=hashed_password, role="student", firstname=item.firstname,lastname=item.lastname, bio=item.bio , contact=item.phone, ssn=item.ssn , year_born=item.birth_year)
        user = await user_repo.add_or_update(user_info)

        user_id = user['id']

        class_info = await class_repo.get_by_id(item.class_id)
        if not class_info:
          raise HTTPException(status_code=404, detail=f"Class with ID {item.class_id} not found")
        class_credit = 4
        class_price = class_info["price"]
        print('s')
        new_enroll = EnrollCreate(student_id=user_id , class_id=item.class_id ,  time=item.time, date_at=datetime.utcnow(), status=0, day=item.day ,credit=class_credit,credit_spent=0)
        new_enroll = await item_repo.create(new_enroll)
        print('x')
        token=request_payment(class_price)
        url = create_pay_url(token)
        pay_token = PayTokenCreate(token=token ,enroll_id=new_enroll.id, created_at= datetime.utcnow() ,expires_at = datetime.utcnow() + timedelta(days=1))
        await pay_token_repo.create(pay_token)

        token_record = generate_jwt(user_id, "student")

        # Save the token in the database
        await token_repo.create(token_record)

        return SubmitEnrollResponse(
            message="enrolled successfully",
            url=url,
            token=token_record.token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/verify/", response_model=VerifyEnrollResponse)
async def verify_enroll(token: str , amount: int , db=Depends(get_db)):
    try:
        pay_token_repo = PayTokenRepository(db)
        pay_request=await pay_token_repo.get_by_token(token)
        
        # Check if the payment token exists
        if not pay_request:
            raise HTTPException(status_code=400, detail="Invalid or expired token.")
        

        # Verify the payment
        answer = verify_payment(token=token, amount=amount)
        
        # Check if the payment was successful
        if not answer:
            raise HTTPException(status_code=400, detail="Payment has not taken place.")
        
        new_payment = PaymentCreate(enroll_id=pay_request['enroll_id'],amount=amount, created_at = datetime.utcnow() )
        payment_repo = PaymentRepository(db)
        await payment_repo.create(new_payment)
        

        # Update the enrolls table
        item_repo = ItemRepository(db)
        new_enroll = await item_repo.update_status(id=pay_request['enroll_id'], status=1)

        # Update the pay_tokens table
        await pay_token_repo.soft_delete(pay_request['id'])

        return VerifyEnrollResponse(
            message="Payment verified successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=UpdateEnrollResponse, dependencies=[Depends(verify_admin)])
async def update_item(item_id: int, item: EnrollUpdate, db=Depends(get_db)):
    try:
        # Instantiate the repository with the connection
        item_repo = ItemRepository(db)
        # Perform the update operation
        result = await item_repo.update(item_id, item)

        if result:
            return UpdateEnrollResponse(
                id=item_id,
                message="Item updated successfully"
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
  
