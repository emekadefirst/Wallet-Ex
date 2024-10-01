from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
from .user import User  


def wallet_tag(username):
    now = datetime.now()
    time_str = now.strftime("%M%S")
    return f"{username}N{time_str}"


class Wallet(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)  
    balance: float | None = Field(default=0.00)
    tag: str | None = Field(max_length=20)
    user: "User" = Relationship(back_populates="wallet")

    def __init__(self, user: User, balance: float = 0.00):
        self.user_id = user.id
        self.balance = balance
        self.tag = wallet_tag(user.username)  

    def __str__(self):
        return self.tag  
