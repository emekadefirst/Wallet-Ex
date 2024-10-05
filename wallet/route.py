from .schemas import Fund, BankSend, AppSend
from fastapi import APIRouter
from .session import add_fund
from pypstk.payment import Payment

wallet = APIRouter()
secret_key = "your secret_key from api"

@wallet.post("/deposit")
async def add_fund(pay: Fund):
    new_payment = Payment(email=pay.email, amount=pay.amount, secret_key=secret_key)
    transaction_data = new_payment.initialize_transaction()
    reference = transaction_data["reference"]
    add_fund(user_id=pay.user_id, amount=pay.amount, reference=reference)
    return transaction_data["url"]


@wallet.post("/app/debit")
async def debit(send: AppSend):
    pass


@wallet.post("/bank/debit")
async def debit(send: BankSend):
    pass
