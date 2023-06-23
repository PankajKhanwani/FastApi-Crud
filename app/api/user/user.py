from typing import List
import secrets
from fastapi.security import HTTPBasicCredentials
from fastapi import APIRouter, Body, HTTPException, Request
from passlib.context import CryptContext

from app.api.user.response_schemas import UserResponseSchema
from app.api.user.schemas import UserSchema
from app.db.mongo import Mongo
from datetime import datetime, timedelta

router = APIRouter()
non_auth_router = APIRouter()

mongo_client: Mongo = Mongo()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@non_auth_router.post('/register', description='Create a new user', response_model=None, status_code=201,
                      response_description="Create User Response")
async def create_user(user: UserSchema):
    """
    Create a new user
    :param user: Field described in the User model
    :return: uuid of the created user
    """
    result = await mongo_client.add('users', user)
    return {'uuid': result}


@router.get('', description='List all users', response_model=List[UserResponseSchema], status_code=200,
            response_description="List Users Response")
async def list_users():
    """
    List all users
    :return: List of users
    """
    result = await mongo_client.find('users', {})
    return result


@router.get('/{uuid}', description='Get a user by uuid', response_model=UserResponseSchema, status_code=200,
            response_description="Get User Response")
async def get_user(uuid: str):
    """
    Get a user by uuid
    :param uuid: User uuid
    :return: User model
    """
    result = await mongo_client.find('users', {'uuid': uuid})
    return result[0]


@router.delete('/{uuid}', description='Delete a user by uuid', response_model=None, status_code=204,
               response_description="Delete User Response")
async def delete_user(uuid: str):
    """
    Delete a user by uuid
    :param uuid: User uuid
    :return: None
    """
    await mongo_client.delete('users', {'uuid': uuid})


@router.put('/{uuid}', description='Update a user by uuid', response_model=None, status_code=200,
            response_description="Update User Response")
async def update_user(uuid: str, name: str = Body(), email: str = Body(),
                      mobile_number: str = Body()):
    """
    Update a user by uuid
    :param uuid: User uuid
    :param user: User model
    :return: User model
    """
    user_obj = await mongo_client.find('users', {'uuid': uuid})
    if not user_obj:
        raise HTTPException(status_code=404, detail='User not found')
    await mongo_client.update('users', uid=uuid,
                              document={'name': name, 'email': email, 'mobile_number': mobile_number})
    return None


@non_auth_router.post('/login', description='Login a user', response_model=dict, status_code=200,
                      response_description="Login User Response")
async def login_user(credentials: HTTPBasicCredentials):
    """
    Login a user
    :param credentials: User credentials
    :return: User model
    """
    result = await mongo_client.find('users', {'email': credentials.username})
    if not result:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    pwd = password_context.hash(credentials.password)
    check_pwd = password_context.verify(credentials.password, result[0]['password'])
    if not check_pwd:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = secrets.token_hex(32)
    user_obj = await mongo_client.find('users', {'uuid': result[0]['uuid']})
    current_date = datetime.now()
    await mongo_client.update('auth_token', user_obj[0]['uuid'], {'token': token,
                                                                  'expires': current_date + timedelta(seconds=3600),
                                                                  'updated_at': current_date,
                                                                  'created_at': current_date},
                              upsert=True)
    return {'access_token': token}


@router.post('/logout', description='Logout a user', response_model=None, status_code=204,
             response_description="Logout User Response")
async def logout_user(request: Request):
    """
    Logout a user
    :return: None
    """
    token = request.headers.get('token')
    await mongo_client.delete('auth_token', {'token': token})
    return
