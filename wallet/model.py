import uuid
import string
import random as r
from enum import Enum
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


class ActionOption(str, Enum):
    TRANSFER = "Transfer"
    ADD = "Add"

class Transactions(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  
    amount: float = Field(default=0.00)
    time: datetime = Field(default_factory=datetime.now)
    action: ActionOption | None = Field(default=None, description="Type of transaction action")
    reference: str | None = Field(max_length=12, unique=True)  
