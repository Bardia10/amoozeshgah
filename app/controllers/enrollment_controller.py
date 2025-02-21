from fastapi import FastAPI, Depends, HTTPException, Request, Header,APIRouter
from app.models.enrollment import EnrollCreate,EnrollResponse,VerifyPayment,VerifyPaymentResponse,Schedule
from app.dependencies.db_dependencies import get_db
from app.auth.auth import hash_password
from app.payment.payment import request_payment,create_pay_url,verify_request
from datetime import datetime,timedelta,time, date
from typing import Optional,List

router = APIRouter()



@router.post("/enroll", response_model=EnrollResponse)
async def submit_enroll(item: EnrollCreate,db=Depends(get_db)):
    try:
        username=item.ssn
        password=str(item.birth_year)
        hashed_password = hash_password(password)
        
        result = await db.fetchrow("""
            INSERT INTO users (username, password_hash, role, firstname, lastname, bio, contact, ssn, year_born)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (username) 
            DO UPDATE SET 
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            contact = EXCLUDED.contact,
            bio = EXCLUDED.bio,
            year_born = EXCLUDED.year_born,
            password_hash = EXCLUDED.password_hash
            RETURNING id
        """, username, hashed_password, "student", item.firstname, item.lastname, item.bio, item.phone, item.ssn, item.birth_year)

        new_id = result["id"]
        # Insert the new item into the items table
        enroll_result = await db.fetchrow(
            "INSERT INTO enrolls (student_id, class_id,day,time,date_at,status,credit,credit_spent) VALUES ($1, $2,$3,$4,$5,$6,$7,$8) RETURNING id",
            new_id,
            item.class_id,
            item.day,
            item.time,
            datetime.utcnow(),
            0,
            4,
            0
        )
        enroll_id = enroll_result["id"]
        amount = await db.fetchrow("SELECT price FROM classes WHERE id = $1", item.class_id)
        token=request_payment(amount["price"])
        url = create_pay_url(token)
        await db.execute(
            "INSERT INTO pay_tokens (token,enroll_id, created_at,is_deleted) VALUES ($1, $2,$3,$4)",
            token,
            enroll_id,
            datetime.utcnow(),
            False
        )

        return EnrollResponse(
            message="enrolled successfully",
            url=url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verify_payment", response_model=VerifyPaymentResponse)
async def verify_payment(token: str , amount: int,db=Depends(get_db) ):
    try:
        pay_request = await db.fetchrow("SELECT * FROM pay_tokens WHERE token = $1", token)
        
        # Check if the payment token exists
        if not pay_request:
            raise HTTPException(status_code=400, detail="Invalid or expired token.")

        # Verify the payment
        answer = verify_request(token=token, amount=amount)
        
        # Check if the payment was successful
        if not answer:
            raise HTTPException(status_code=400, detail="Payment has not taken place.")

        # Update the enrolls table
        await db.execute(
            "UPDATE enrolls SET status = 1 WHERE id = $1",
            pay_request["enroll_id"]
        )

        # Update the pay_tokens table
        await db.execute(
            "UPDATE pay_tokens SET is_deleted = TRUE, deleted_at = $1 WHERE id = $2",
            datetime.utcnow(),
            pay_request["id"]
        )

        return VerifyPaymentResponse(
            message="Payment verified successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await db.close()