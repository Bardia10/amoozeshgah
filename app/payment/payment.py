# app/payments/payment.py

merchant_id = "mervh123"

def request_payment(amount: int):
    callback_url = "google.com"
    token = merchant_id + callback_url + str(amount)
    return token

def create_pay_url(token: str):
    url = "google.com/" + token
    return url

def verify_request(token, amount):
  return True