import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from database import engine
from .schemas import TokenData
from .models import User, Credentials, Admin
from .config import (
    get_password_hash,
    verify_password,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)
from sqlmodel import Session, select

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
        user = session.exec(select(User).where(User.email == email)).first()
        if user and verify_password(password, user.password):
            return user
        else:
            raise Exception("Invalid credentials")


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
    street,
    city,
    zip_code,
    state,
    id_document,
    country,
    phone_number,
    user_id,
):
    with Session(engine) as session:
        detail = Credentials(
            street=street,
            city=city,
            zip_code=zip_code,
            state=state,
            id_document=id_document,
            country=country,
            phone_number=phone_number,
            user_id=user_id,
        )
        session.add(detail)
        session.commit()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = user_get_user_by_id(id=id)
    if user is None:
        raise credentials_exception
    return user


def create_admin(email, username, password):
    with Session(engine) as session:
        model = Admin(email=email, username=username, password=password)
        session.add(model)
        session.commit()
        user_id = model.id
        return user_id


def get_admin_by_id(id):
    with Session(engine) as session:
        user = session.exec(select(Admin).where(Admin.id == id)).one()
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return data


def login_admin(username, password):
    with Session(engine) as session:
        user = session.exec(select(Admin).where(Admin.username == username)).first()
        if user and verify_password(password, user.password):
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_staff": user.is_staff
            }
        else:
            raise Exception("Invalid credentials")
