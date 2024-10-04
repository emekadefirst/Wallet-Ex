import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from typing import Annotated
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from database import engine
from .models import User, Credentials
from .config import (
    verify_password,
    get_password_hash,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)
from sqlmodel import Session, select


async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print(f"Decoded user ID: {user_id}")  # Log decoded ID
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID missing in token")
        return get_user_by_id(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def create_user(email, username, password):
    with Session(engine) as session:
        model = User(email=email, username=username, password=password)
        session.add(model)
        session.commit()
        user_id = model.id
        return user_id


def all_users():
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()  
        return users


def get_user_by_id(id):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).one()
        return user


def user_get_user_by_id(id):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).one()
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_verified": user.credential_status
        }
        return data


def login_user(email, password):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one()
        if user:
            if verify_password(password, user.password):
                print(user.password)
                return user_get_user_by_id(user.id)
            return "Invalid user details provided"
        return "User not found"


def delete_user(id):
    with Session(engine) as session:
        model = select(User).where(User.id == id)
        data = session.exec(model)
        user = data.one()
        session.delete(user)
        session.commit()


def update_user(id, email=None, username=None, password=None):
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.id == id)).one()
            if email:
                user.email = email
            if username:
                user.username = username
            if password:
                user.password = get_password_hash(password)
            session.commit()
        except Exception as e:
            return f"{e}"


def save_credentials(
    first_name,
    last_name,
    other_name,
    dob,
    street,
    city,
    zip_code,
    state,
    id_document,
    profile_image,
    country,
    phone_number_1,
    phone_number_2,
    user_id,
):
    with Session(engine) as session:
        detail = Credentials(
            first_name=first_name,
            last_name=last_name,
            other_name=other_name,
            dob=dob,
            street=street,
            city=city,
            zip_code=zip_code,
            state=state,
            id_document=id_document,
            profile_image=profile_image,
            country=country,
            phone_number_1=phone_number_1,
            phone_number_2=phone_number_2,
            user_id=user_id,
        )
        session.add(detail)
        session.commit()
