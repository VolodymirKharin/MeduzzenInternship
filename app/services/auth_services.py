from fastapi import HTTPException

from sqlalchemy.sql import insert

from models.models import User
from databases import Database

from utils.security import hash
from datetime import datetime
from fastapi import Depends
from schemas.schemas import ResultUser, UserScheme
from db.db_connection import get_db

from utils.token_verify import VerifyToken, decode_access_token
from services.services import UserServices

from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()


async def get_current_user(token: str = Depends(token_auth_scheme), db: Database = Depends(get_db)) -> UserScheme:
    user_service = UserServices(db=db)
    result = VerifyToken(token.credentials).verify()
    if result.get('status'):
        try:
            email_from_jwt = decode_access_token(encoded_jwt=token)
            user = await user_service.get_user_by_email(email_from_jwt)
            print("$$$$$$$", user.result)
            return user.result
        except:
            raise HTTPException(status_code=401, detail='Wrong token')
    else:
        email_from_auth = result.get('email')
        new_user = await user_service.get_user_by_email(email_from_auth)
        if not new_user:
            new_user = await create_user_from_auth(email_from_auth)
            return new_user
        return new_user.result


async def create_user_from_auth(email: str, db: Database = Depends(get_db)) -> ResultUser:
    new_password = "1234"
    new_user = {
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "user_name": email,
        "user_email": email,
        "user_password": hash.encrypt_password(password=new_password),
        "user_status": True,

    }
    query = insert(User).values(new_user)
    user_service = UserServices(db=db)
    user_id = await get_db().execute(query=query)
    new_user_db = await user_service().get_user(user_id)
    return new_user_db

