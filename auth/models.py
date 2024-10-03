import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str | None = Field(unique=True, max_length=20)
    email: str | None = Field(unique=True, max_length=30)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    credential_status: bool | None = Field(default=False)
    def __str__(self):
        return self.username


class CredentialStatus(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: bool | None = Field(default=False)
    user_id: int = Field(default=None, foreign_key="user.id")


    def __str__(self):
        return self.status


class Credentials(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(max_length=55)
    last_name: str | None = Field(max_length=55)
    other_name: str | None = Field(max_length=55)
    dob: datetime | None = Field(default=None)
    street: str | None = Field(max_length=100)
    city: str | None = Field(max_length=50)
    zip_code: str | None = Field(max_length=50)
    state: str | None = Field(max_length=50)
    id_document: str | None = Field(max_length=500)
    profile_image: str | None = Field(max_length=500)
    country: str | None = Field(max_length=50)
    phone_number_1: str | None = Field(max_length=15)
    phone_number_2: str | None = Field(max_length=15)
    user_id: int = Field(foreign_key="user.id")


class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(unique=True, max_length=20)
    email: str | None = Field(unique=True, max_length=55)
    password: str
    created_at: datetime = Field(default_factory=datetime.date)
    is_staff: bool = Field(default=True)

    def __str__(self):
        return self.username
