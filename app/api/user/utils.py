from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from app.db.mongo import Mongo

mongo_client: Mongo = Mongo()


async def validate_token(token: str = Header()):
    """
    Validate token
    """
    result = await mongo_client.find('auth_token', {'token': token})
    if result:
        current_time = datetime.now()
        expiry = result[0]['expires']
        if expiry > datetime.now():
            result[0]['expires'] = current_time + timedelta(seconds=3600)
            result[0]['updated_at'] = current_time
            await mongo_client.update('auth_token', result[0]['uuid'], result[0])
            return result[0]
        else:
            raise HTTPException(status_code=401, detail="Token Expired")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
