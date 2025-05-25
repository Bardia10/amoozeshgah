from config.settings import settings
from app.services.pseudo_paypal import create_paypal, check_paypal
from datetime import datetime


merchant_id	= settings.merchant_id

async def request_payment(amount:int, db):
    callback_url = settings.callback_url
    token = merchant_id+str(amount)+datetime.now().strftime("%H:%M:%S")

    await create_paypal(token , amount, db)
    return token

def create_pay_url(token:str):
    url = settings.pay_url + token
    return url

async def verify_payment(token:str, amount:int,db):
  return await check_paypal(token, amount, db)