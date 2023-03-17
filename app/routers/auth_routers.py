from starlette import status


from fastapi import APIRouter, HTTPException, Depends
from schemas.schemas import SignInRequest, TokenResponse, Token, UserSchemeToken, ResultUserToken
from services.auth_services import get_current_user
from services.services import UserServices
from utils.security import Hasher
from utils.token_verify import create_access_token
from db.db_connection import get_db
from databases import Database


auth_routers = APIRouter()


@auth_routers.get('/auth/me', tags=["auth0"], response_model=ResultUserToken, status_code=status.HTTP_200_OK)
async def get_me(current_user=Depends(get_current_user)) -> ResultUserToken:
    return ResultUserToken(result=UserSchemeToken(
                                        user_id=current_user.user_id,
                                        user_email=current_user.user_email,
                                        user_name=current_user.user_name,
                                        user_status=current_user.user_status
    )
    )


@auth_routers.post("/auth/login", tags=["auth0"], response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user_in: SignInRequest, db: Database = Depends(get_db)):
    user_service = UserServices(db=db)
    user = await user_service.get_user_by_email(user_email=user_in.user_email)
    if not user:
        raise HTTPException(status_code=401, detail='not autorize, wrong pass or email')
    user_hashed_password = await user_service.get_user_password(user_email=user_in.user_email)
    if user is None or not Hasher.check_encrypted_password(password=user_in.user_password, hashed=user_hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    return TokenResponse(result=Token(access_token=create_access_token(user_email=user.result.user_email), token_type="Bearer"))










