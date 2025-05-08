from config.settings import settings


merchant_id	= "mervh123"

def request_payment(amount:int):
    callback_url = settings.callback_url
    token = merchant_id+callback_url+str(amount)
    return token

def create_pay_url(token:str):
    url = settings.pay_url + token
    return url

def verify_payment(token, amount):
  return True