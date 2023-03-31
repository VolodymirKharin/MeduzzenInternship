import random

from databases import Database

from fastapi import Depends, HTTPException
from schemas.user_schemas import ResultUser, UserScheme, SignUpRequest
from db.db_connection import get_db

from utils.token_verify import VerifyToken, decode_access_token
from services.user_services import UserServices

from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()


async def get_current_user(token: str = Depends(token_auth_scheme), db: Database = Depends(get_db)) -> UserScheme:
    user_service = UserServices(db=db)
    result = VerifyToken(token.credentials).verify()
    if result.get('status'):
        try:
            email_from_jwt = decode_access_token(encoded_jwt=token)
            user = await user_service.get_user_by_email(email_from_jwt)
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


async def create_user_from_auth(email: str) -> ResultUser:
    new_password = str(round(random.SystemRandom().random(), 5))
    obj_user_model = UserServices(db=get_db())
    created_user = await obj_user_model.create_user(user=SignUpRequest(user_name=email,
                                                                       user_email=email,
                                                                       user_password=new_password,
                                                                       user_password_repeat=new_password,
                                                                       user_status=True
                                                                       )
                                                    )
    return created_user.result
