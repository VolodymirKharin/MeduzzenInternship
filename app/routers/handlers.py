from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from schemas.schemas import UserUpdateRequest, SignUpRequest, Results, ResultUser
from services.services import UserServices
from db.db_connection import get_db
from databases import Database

router = APIRouter()


@router.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@router.get("/users", response_model=Results)
async def get_users(db: Database = Depends(get_db)) -> Results:
    user_service = UserServices(db=db)
    users_list = await user_service.get_users()
    return users_list


@router.get("/user", response_model=ResultUser)
async def get_user(user_id: int, db: Database = Depends(get_db)) -> ResultUser:
    user_service = UserServices(db=db)
    user_db = await user_service.get_user(user_id=user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail='User does not exist')
    return user_db


@router.post("/user", response_model=ResultUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: SignUpRequest, db: Database = Depends(get_db)) -> ResultUser:
    user_service = UserServices(db=db)
    new_user = await user_service.create_user(user=user)
    if not new_user:
        raise HTTPException(status_code=422, detail='User already exist')
    return new_user


@router.put("/user", response_model=ResultUser, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdateRequest, db: Database = Depends(get_db)) -> ResultUser:
    user_service = UserServices(db=db)
    updated_user = await user_service.update_user(user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    return updated_user


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Database = Depends(get_db)):
    user_service = UserServices(db=db)
    await user_service.delete_user(user_id=user_id)

