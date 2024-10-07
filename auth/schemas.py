from typing import Optional
from pydantic import BaseModel
from typing import Annotated, Union
import shutil
from fastapi import UploadFile, Form, File, UploadFile


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class SignUp(BaseModel): 
    email: str 
    username: str 
    password: str 


class Login(BaseModel): 
    email: str 
    password: str 


class CredentialsSchema(BaseModel): 
    first_name: str 
    last_name: str 
    other_name: str  
    dob: str 
    city: str
    zip_code: str 
    state: str 
    id_document: Optional[UploadFile] = (File(None),)
    profile_image: Optional[UploadFile] = (File(None),)
    street: str
    country: str 
    phone_number_1: str
    phone_number_2: str 
    user_id: str 
