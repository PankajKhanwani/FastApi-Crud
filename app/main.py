import logging
import traceback

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

logging.getLogger().setLevel(logging.DEBUG)
LOG = logging.getLogger(__name__)

from app.api import auth_router

app = FastAPI(openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs', redoc_url='/api/v1/redoc',
              title='User Crud', description='User Crud', version='1.0.0', debug=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth_router)
@app.middleware("http")
async def app_middleware(request, call_next):
    """
    Middleware for App
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        LOG.error(e)
        traceback.print_exc()
        return JSONResponse(content="Something went wrong", status_code=500)


