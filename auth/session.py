from database import engine
from .models import User
from .config import verify_password, get_password_hash
from sqlmodel import Session, select


def create_user(email, username, password):
    with Session(engine) as session:
        model = User(email=email, username=username, password=password)
        session.add(model)
        session.commit()
        user_id = model.id
        return user_id


def all_user():
    with Session(engine) as session:
        model = select(User)
        users = session.exec(model)
        for user in users:
            print(user)


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
