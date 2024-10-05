from pydantic import BaseModel

class Fund(BaseModel):
    email: str
    amount: float
    user_id: int
    action: str


class AppSend(BaseModel):
    amount: float
    user_id: int
    recipient_email: str


class BankSend(BaseModel):
    amount: float
    user_id: int
    account_number: int
    bank_name: str
