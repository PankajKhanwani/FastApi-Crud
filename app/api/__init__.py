from fastapi import APIRouter, Depends
from app.api.user import user
from app.api.user.utils import validate_token

auth_router = APIRouter()
auth_router.include_router(user.router, prefix="/user", tags=["user"], dependencies=[Depends(validate_token)])
auth_router.include_router(user.non_auth_router, prefix="/user", tags=["user"])
