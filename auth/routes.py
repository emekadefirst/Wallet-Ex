from dotenv import load_dotenv
from .schemas import SignUp, Login, AdminSignUp, AdminLogin
from decorators import admin_required
from .config import get_password_hash, create_access_token
from .session import (
    create_user,
    user_get_user_by_id,
    login_user,
    all_users,
    get_current_user,
    create_admin,
    get_admin_by_id,
    login_admin,
)
from fastapi import APIRouter, status, HTTPException, Request


load_dotenv()
auth = APIRouter()

@auth.post("/login")
async def login(login: Login, request: Request):
    token = request.headers.get("access_token")
    if token:
        current_user_id = await get_current_user(token)
        user = login_user(email=login.email, password=login.password)
        if user:
            data = user_get_user_by_id(user.id)
            return {
                "detail": "Login successful",
                "status": status.HTTP_200_OK,
                "token_type": "bearer",
                "access_token": token,
                "data": data
            }
        return {"message": "invalid credentials", "status": status.HTTP_400_BAD_REQUEST}
    return {"message": "Unauthorized", "status": status.HTTP_401_UNAUTHORIZED}


@auth.post("/signup")
def register(user: SignUp):
    data = create_user(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
    )
    if data:
        detail = user_get_user_by_id(data)
        user_data = {"id": data}
        print(user_data)
        access_token = create_access_token(user_data)
        return {
            "status": status.HTTP_201_CREATED,
            "data": detail,
            "access_token": access_token,
            "token_type": "bearer",
        }
    return status.HTTP_400_BAD_REQUEST


@auth.post("/logout")
def logout():
    return {"detail": "Logout successful"}


@auth.get("/admin/all-users")
@admin_required
def admin_all_users():
    users = all_users()
    if users:
        return {
            "status": status.HTTP_200_OK,
            "data": [
                {
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "is_verified": user.credential_status,
                }
                for user in users
            ],
        }
    return {"status": status.HTTP_404_NOT_FOUND, "message": "No users found"}


@auth.get("/profile/{id}")
def user_profile_by_id(id : int):
    user = user_get_user_by_id(id)
    if user:
        return {"status": status.HTTP_200_OK, "data": user}
    return {"detail": "User not found", "status": status.HTTP_404_NOT_FOUND}


@auth.put("/reset-password")
def reset():
    pass

@auth.post("/admin-signup")
def admin_signup(signup : AdminSignUp):
    admin_session = create_admin(
        username=signup.username,
        email=signup.email,
        password=get_password_hash(signup.password),
    )
    if admin_session:
        data = get_admin_by_id(admin_session)
        return {
            "status": status.HTTP_201_CREATED,
            "data": data
        }
    return {"status": status.HTTP_400_BAD_REQUEST, "detail": "Error during signup"}

@auth.post("/admin-login")
def admin_login(login: AdminLogin):
    user = login_admin(username=login.username, password=login.password)
    if user:
        return {"status": status.HTTP_200_OK, "data": user}
    return {"status": status.HTTP_400_BAD_REQUEST, "detail": "Wrong credentails provided"}

