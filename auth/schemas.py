from pydantic import BaseModel
from typing import Annotated, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


class SignUp(BaseModel): 
    email: str 
    username: str 
    password: str 


class Login(BaseModel): 
    email: str 
    password: str 


class CredentialsSchema(BaseModel): 
    id: int
    first_name: str 
    last_name: str 
    other_name: str  
    dob: str 
    city: str
    zip_code: str 
    state: str 
    id_document: str 
    profile_image: str 
    country: str 
    phone_number_2: str 
    user_id: str 
