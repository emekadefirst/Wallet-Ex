import uuid
import string
import random as r
from datetime import datetime
from sqlmodel import SQLModel, Field


def wallet_tag():
    now = datetime.now()
    time_str = now.strftime("%M%S")
    upper_letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    first_letter = "".join(r.sample(upper_letters, 2))
    second_letter = "".join(r.sample(lower_letters, 2))
    all_values = first_letter + second_letter 
    strand = list(all_values)
    r.shuffle(strand)
    return f"NGN{strand}{time_str}"


class Wallet(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    balance: float | None = Field(default=0.00)
    tag: str | None = Field(max_length=20, default=wallet_tag)

    def __str__(self):
        return self.tag


class Credit(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  
    amount: float = Field(default=0.00)
    reference: str | None = Field(max_length=12, unique=True)
    status: str | None = Field(max_length=12, default="processing")
    time: datetime = Field(default_factory=datetime.now)


    def __str__(self):
        return self.reference

class Debit(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: float = Field(default=0.00)
    creditor: str | None = Field(max_length=12, unique=True)
    status: str | None = Field(max_length=12, default="processing")
    time: datetime = Field(default_factory=datetime.now)


class Transactions(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
