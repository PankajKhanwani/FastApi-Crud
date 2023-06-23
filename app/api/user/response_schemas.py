from pydantic import BaseModel, validator
from datetime import datetime


class Base(BaseModel):
    """
    Base model
    """
    created_at: datetime = None
    updated_at: datetime = None

    @validator('created_at', 'updated_at')
    def validate_dates(cls, value):
        """
        Validate dates
        """
        value = value.strftime("%Y-%m-%d %H:%M:%S")
        return value


class UserResponseSchema(Base):
    """
    User model
    """
    uuid: str
    name: str
    email: str
    mobile_number: str
