from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
from ..auth.user import User
from typing import Optional


class Credentials(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(max_length=55)
    last_name: str | None = Field(max_length=55)
    other_name: str | None = Field(max_length=55)
    dob: datetime | None = Field(default=None)  
    street: str | None = Field(max_length=100)  
    city: str | None = Field(max_length=50)  
    state: str | None = Field(max_length=50)  
    country: str | None = Field(max_length=50)  
    phone_number_1: str | None = Field(max_length=15)  
    phone_number_2: str | None = Field(max_length=15)  
    user_id: int = Field(foreign_key="user.id")  
    user: User = Relationship(back_populates="credentials")  

    
    @property
    def email(self) -> Optional[str]:
        return self.user.email if self.user else None



