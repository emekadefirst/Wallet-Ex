from pydantic import BaseModel
from typing import Annotated, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    email: str
    username: str
    password: str


class Login(BaseModel):
    email: str
    password: str


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CredentialsSchema(BaseModel):
    id: Optional[int] = Field(
        default=None, description="The primary key of the credentials"
    )
    first_name: Optional[str] = Field(
        None, max_length=55, description="User's first name"
    )
    last_name: Optional[str] = Field(
        None, max_length=55, description="User's last name"
    )
    other_name: Optional[str] = Field(
        None, max_length=55, description="User's other name"
    )
    dob: Optional[datetime] = Field(None, description="User's date of birth")
    street: Optional[str] = Field(
        None, max_length=100, description="User's street address"
    )
    city: Optional[str] = Field(None, max_length=50, description="User's city")
    zip_code: Optional[str] = Field(None, max_length=50, description="User's zip code")
    state: Optional[str] = Field(None, max_length=50, description="User's state")
    id_document: Optional[str] = Field(
        None, max_length=500, description="User's ID document"
    )
    profile_image: Optional[str] = Field(
        None, max_length=500, description="User's profile image"
    )
    country: Optional[str] = Field(None, max_length=50, description="User's country")
    phone_number_1: Optional[str] = Field(
        None, max_length=15, description="User's primary phone number"
    )
    phone_number_2: Optional[str] = Field(
        None, max_length=15, description="User's secondary phone number"
    )
    user_id: int = Field(..., description="The ID of the associated user")

    class Config:
        orm_mode = True
