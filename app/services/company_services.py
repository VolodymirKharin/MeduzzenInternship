from fastapi import HTTPException

from sqlalchemy.sql import select, insert, update, delete
from models.models import Company
from schemas.company_schemas import ResultCompany, CompanyScheme, SignUpCompany, Results, CompanyListResponse, CompanyUpdateRequest
from databases import Database


from datetime import datetime


class CompanyServices:
    def __init__(self, db: Database):
        self.db = db

    async def get_companies(self, current_user_id: int) -> Results:
        query = select(Company).where(Company.owner_id == current_user_id)
        company_list = await self.db.fetch_all(query=query)
        result = CompanyListResponse(companies=[CompanyScheme(**item) for item in company_list])
        return Results(result=result)

    async def get_company(self, company_id: int, current_user_id: int) -> ResultCompany:
        query = select(Company).where(Company.company_id == company_id and Company.current_user_id == current_user_id)
        company = await self.db.fetch_one(query=query)
        if not company:
            raise HTTPException(status_code=404, detail='Company does not exist')
        return ResultCompany(result=CompanyScheme(**dict(company)))

    async def create_company(self, company: SignUpCompany, current_user_id: int) -> ResultCompany:
        new_company = {
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "company_name": company.company_name,
            "company_description": company.company_description,
            "owner_id": current_user_id
        }
        query = insert(Company).values(new_company)
        company_id = await self.db.execute(query=query)
        new_company_db = await self.get_company(company_id=company_id, current_user_id=current_user_id)
        return new_company_db

    async def delete_company(self, company_id: int, current_user_id: int):
        query = delete(Company).where(Company.company_id == company_id and Company.current_user_id == current_user_id)
        await self.db.execute(query=query)

    async def update_company(self, company_id: int, company: CompanyUpdateRequest, current_user_id: int) -> ResultCompany:
        update_data = {
            "company_name": company.company_name,
            "company_description": company.company_description,
        }
        query = update(Company).where(Company.company_id == company_id and Company.current_user_id == current_user_id).values(update_data)
        await self.db.execute(query=query)
        updated_company = await self.get_company(company_id=company_id, current_user_id=current_user_id)

        return updated_company

