import os
import time
from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from .schemas import Fund, BankSend, AppSend
from .session import add_fund, update_balance, update_status
from pypstk.payment import Payment
from pypstk.status import Verify
from dotenv import load_dotenv

load_dotenv()
wallet = APIRouter()
secret_key = os.environ.get('PAYSTACK_KEY')


@wallet.post("/deposit")
async def add_fund(pay: Fund, background_tasks: BackgroundTasks):
    try:
        new_payment = Payment(email=pay.email, amount=pay.amount, secret_key=secret_key)
        print(secret_key)
        transaction_data = new_payment.initialize_transaction()

        if transaction_data:
            reference = transaction_data["reference"]
            add_fund(user_id=pay.user_id, amount=pay.amount, reference=reference)
            background_tasks.add_task(
                verify_payment,
                reference=reference,
                user_id=pay.user_id,
                amount=pay.amount,
            )
            return {"payment_url": transaction_data["url"], "reference": reference}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to initialize transaction",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def verify_payment(reference: str, user_id: int, amount: float):
    try:
        trial_limit = 10
        count = 0

        while count < trial_limit:
            verify = Verify(reference=reference, secret_key=secret_key)
            response = verify.status()

            if response == "success":
                update_balance(user_id=user_id, amount=amount)
                update_status(status="success", reference=reference)
                return {
                    "message": "Deposit successful.",
                    "status": status.HTTP_201_CREATED,
                }
            elif response == "pending":
                time.sleep(5)
                count += 1
            else:
                update_status(status="failed", reference=reference)
                return {
                    "message": "Deposit failed.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
        update_status(status="failed", reference=reference)
        return {"message": "Failed to verify transaction after multiple attempts."}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@wallet.post("/app/debit")
async def debit(send: AppSend):
    pass


@wallet.post("/bank/debit")
async def debit(send: BankSend):
    pass
