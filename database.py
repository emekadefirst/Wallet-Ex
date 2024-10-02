from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, create_engine
from auth.models import User, Admin, Credentials, CredentialStatus
from wallet.model import Wallet


def create_db():
    db_url = 'expendier.db'
    engine = create_engine(f"sqlite:///{db_url}", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine
engine = create_db()
