import os
from dotenv import load_dotenv
from .schemas import SignUp, Login
from .config import get_password_hash
from .session import create_user, user_get_user_by_id, login_user
from fastapi import APIRouter, status, HTTPException


load_dotenv()
auth = APIRouter()


@auth.post("/login")
def login(login: Login):
    user = login_user(email=login.email, password=login.password)
    if user is not None:
        return  {"detail": user, "status": status.HTTP_200_OK}
    return {"detail": user, "status": status.HTTP_401_UNAUTHORIZED}


@auth.post("/signup")
def register(user: SignUp):
    if user:
        user_id = create_user(
            email=user.email,
            username=user.username,
            password=get_password_hash(user.password),
        )
        data = user_get_user_by_id(user_id)
        return {"status": status.HTTP_201_CREATED, "data": data}
    return status.HTTP_400_BAD_REQUEST


@auth.post("/logout")
def logout():
    pass
