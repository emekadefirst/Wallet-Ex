from datetime import datetime
from sqlmodel import SQLModel, Field
from database import create_db


class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(unique=True, max_length=20)
    email: str | None = Field(unique=True, max_length=55)
    password: str
    created_at: datetime = Field(default_factory=datetime.now())
    is_staff: bool = Field(default=True)

    def __str__(self):
        return self.username
