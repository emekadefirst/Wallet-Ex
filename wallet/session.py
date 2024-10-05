from database import engine
from typing import Optional
from .model import Credit, Wallet, Debit
from sqlmodel import Session, select


def add_fund(user_id: int, amount: float, reference: str):
    with Session(engine) as session:
        detail = Credit(user_id=user_id, amount=amount, reference=reference)
        session.add(detail)
        session.commit()


def update_status(status: Optional[str] = None, reference: Optional[str] = None):
    with Session(engine) as session:
        detail = session.exec(select(Credit).where(Credit.reference == reference)).one()
        if not detail:
            raise ValueError("Fund record not found for this user.")
        if status is not None:
            detail.status = status
        session.add(detail)  
        session.commit()


def update_balance(amount: Optional[int] = None, tag: Optional[str] = None):
    with Session(engine) as session:
        detail = session.exec(select(Wallet).where(Wallet.tag == tag)).one()
        if not detail:
            raise ValueError("Invalide wallet tag")
        if amount:
            detail.balance = amount
        session.add(detail)
        session.commit()
