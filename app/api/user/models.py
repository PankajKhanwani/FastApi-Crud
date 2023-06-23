from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    """
    Base model
    """
    created_at: datetime = datetime.now()
    updated_at: datetime = None


class UserModel(Base):
    """
    User model
    """
    name: str
    email: str
    password: str
    mobile_number: str
