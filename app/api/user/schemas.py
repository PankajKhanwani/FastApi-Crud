from pydantic import BaseModel, Field, validate_email, validator
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSchema(BaseModel):
    """
    User model
    """
    email: str = Field(..., description='Email of user', min_length=5, max_length=50)
    repeat_password: str = Field(..., description='Password of user', min_length=8, max_length=50)
    password: str = Field(..., description='Password of user', min_length=8, max_length=50)
    name: str = Field(..., description='Name of user')
    mobile_number: str = Field(..., description='Mobile number of user')

    @validator('email')
    def validate_user_email(cls, value):
        """

        :param value:
        :return:
        """
        validate_email(value)
        return value

    @validator('password')
    def validate_password(cls, value, values):
        """
        Validate password
        :param value: Value contains the repeat password value
        :param values: Values contain the fields which are written above repeat password field in the class
        :return: hash value of the password
        """
        if value != values['repeat_password']:
            raise ValueError('Passwords do not match')
        return password_context.hash(value)
