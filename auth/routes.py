import os
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

load_dotenv()
auth = APIRouter()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

@auth.post("/login")
def login():
    pass


@auth.post("/signup")
def register():
    pass


@auth.post("/logout")
def logout():
    pass
