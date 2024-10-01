from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
from ..wallet.wallet_model import Wallet
from ..wallet.profile_model import Credentials


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(unique=True, max_length=20)
    email: str | None = Field(unique=True, max_length=55)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    status: "UserStatus" = Relationship(back_populates="user", uselist=False)
    wallet: "Wallet" = Relationship(back_populates="user", uselist=False)
    credentials: Credentials = Relationship(back_populates="user", uselist=False)

    def __str__(self):
        return self.username


class UserStatus(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: bool | None = Field(default=False)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="status")

    def __str__(self):
        return f"{self.user.username} {self.status}"
