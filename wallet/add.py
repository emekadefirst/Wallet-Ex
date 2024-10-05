from pydantic import BaseModel
from pypstk.payment import Payment
from fastapi import APIRouter
from .model import Transactions

wallet = APIRouter()
secret_key = "your secret_key from api"

class Pay(BaseModel):
    email : str
    amount : float
    user_id : int
    action : str


@wallet.post("/add")
async def add_fund(pay : Pay):
    new_payment = Payment(email=pay.email, amount=pay.amount, secret_key=secret_key)
    transaction_data = new_payment.initialize_transaction()
    reference = transaction_data['reference']
    save_payment = Transactions()
    return transaction_data['url']

