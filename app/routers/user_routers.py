from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from schemas.schemas import UserUpdateRequest, SignUpRequest, Results, ResultUser
from services.services import UserServices
from db.db_connection import get_db
from databases import Database
from services.auth_services import get_current_user
user_routers = APIRouter()


@user_routers.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@user_routers.get("/users", tags=["User"], response_model=Results)
async def get_users(db: Database = Depends(get_db), current_user=Depends(get_current_user)) -> Results:
    user_service = UserServices(db=db)
    users_list = await user_service.get_users()
    return users_list


@user_routers.get("/user", tags=["User"], response_model=ResultUser)
async def get_user(user_id: int, db: Database = Depends(get_db), current_user=Depends(get_current_user)) -> ResultUser:
    user_service = UserServices(db=db)
    user_db = await user_service.get_user(user_id=user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail='User does not exist')
    return user_db


@user_routers.post("/user", tags=["User"], response_model=ResultUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: SignUpRequest, db: Database = Depends(get_db)) -> ResultUser:
    user_service = UserServices(db=db)
    new_user = await user_service.create_user(user=user)
    if not new_user:
        raise HTTPException(status_code=422, detail='User already exist')
    return new_user


@user_routers.put("/user", tags=["User"], response_model=ResultUser, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdateRequest, current_user=Depends(get_current_user), db: Database = Depends(get_db)) -> ResultUser:
    check_user_id = current_user.user_id
    if user_id != check_user_id:
        raise HTTPException(status_code=403, detail="It's not your account")
    user_service = UserServices(db=db)
    updated_user = await user_service.update_user(user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    return updated_user


@user_routers.delete("/user", tags=["User"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Database = Depends(get_db), current_user=Depends(get_current_user)):
    check_user_id = current_user.user_id
    if user_id != check_user_id:
        raise HTTPException(status_code=403, detail="It's not your account")
    user_service = UserServices(db=db)
    await user_service.delete_user(user_id=user_id)





