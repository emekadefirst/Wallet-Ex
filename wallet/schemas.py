from pydantic import BaseModel

class Fund(BaseModel):
    email: str
    amount: float
    user_id: int


class AppSend(BaseModel):
    amount: float
    recipient_email: str


class BankSend(BaseModel):
    amount: float
    user_id: int
    account_number: int
    bank_name: str
