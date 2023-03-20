from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from schemas.company_schemas import SignUpCompany, CompanyUpdateRequest, ResultCompany, Results
from services.company_services import CompanyServices
from db.db_connection import get_db
from databases import Database
from services.auth_services import get_current_user

company_routers = APIRouter()


@company_routers.get("/companies", tags=["Company"], response_model=Results)
async def get_users(db: Database = Depends(get_db), current_user=Depends(get_current_user)) -> Results:
    company_service = CompanyServices(db=db)
    users_list = await company_service.get_companies(current_user_id=current_user.user_id)
    return users_list


@company_routers.get("/company/{company_id}", tags=["Company"], response_model=ResultCompany, status_code=status.HTTP_200_OK)
async def get_company(company_id: int, db: Database = Depends(get_db), current_user=Depends(get_current_user)) -> ResultCompany:
    if not current_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    company_service = CompanyServices(db=db)
    company_db = await company_service.get_company(company_id=company_id, current_user_id=current_user.user_id)
    return company_db


@company_routers.post("/company", tags=["Company"], response_model=ResultCompany, status_code=status.HTTP_201_CREATED)
async def create_company(company: SignUpCompany, db: Database = Depends(get_db), current_user=Depends(get_current_user)) -> ResultCompany:
    if not current_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    company_service = CompanyServices(db=db)
    new_company = await company_service.create_company(company=company, current_user_id=current_user.user_id)
    return new_company


@company_routers.put("/company/{company_id}", tags=["Company"], response_model=ResultCompany, status_code=status.HTTP_200_OK)
async def update_company(company_id: int, company: CompanyUpdateRequest, current_user=Depends(get_current_user), db: Database = Depends(get_db)) -> ResultCompany:
    company_service = CompanyServices(db=db)
    updated_user = await company_service.update_company(company_id=company_id, company=company, current_user_id=current_user.user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail='Company does not exist')
    return updated_user


@company_routers.delete("/company/{company_id}", tags=["Company"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: Database = Depends(get_db), current_user=Depends(get_current_user)):
    current_user_id = current_user.user_id
    company_service = CompanyServices(db=db)
    await company_service.delete_company(company_id=company_id, current_user_id=current_user_id)





