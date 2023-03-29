from fastapi import HTTPException

from sqlalchemy.sql import select, insert, update, delete
from models.models import Company
from schemas.schemas import UserScheme
from schemas.company_schemas import ResultCompany, CompanyScheme, SignUpCompany, Results, CompanyListResponse, CompanyUpdateRequest
from databases import Database

from services.user_services import UserServices

from datetime import datetime


class CompanyServices:
    def __init__(self, db: Database, current_user: UserScheme = None):
        self.db = db
        self.current_user_id = None if not current_user else current_user.user_id

    async def get_companies(self) -> Results:
        await self.check_current_user()
        company_list = await self.db.fetch_all(query=select(Company))
        result = CompanyListResponse(companies=[CompanyScheme(**item) for item in company_list])
        return Results(result=result)

    async def get_company(self, company_id: int) -> ResultCompany:
        await self.check_current_user()
        company = await self.check_for_company_existing(company_id=company_id)
        return ResultCompany(result=company)

    async def create_company(self, company: SignUpCompany) -> ResultCompany:
        await self.check_company_name(company_name=company.company_name)
        datetime_now = datetime.now()
        new_company = {
            "created_at": datetime_now,
            "updated_at": datetime_now,
            "company_name": company.company_name,
            "company_description": company.company_description,
            "owner_id": self.current_user_id
        }
        query = insert(Company).values(new_company)
        company_id = await self.db.execute(query=query)
        return ResultCompany(result=CompanyScheme(company_id=company_id,
                                                  company_name=company.company_name,
                                                  company_description=company.company_description,
                                                  created_at=datetime_now,
                                                  updated_at=datetime_now,
                                                  owner_id=self.current_user_id


        )
        )

    async def delete_company(self, company_id: int):
        await self.check_company_for_exist(company_id=company_id)
        await self.check_for_owner(company_id=company_id)
        query = delete(Company).where(Company.company_id == company_id)
        await self.db.execute(query=query)

    async def check_company_for_exist(self, company_id: int):
        query = select(Company).where(Company.company_id == company_id)
        company_db = await self.db.fetch_one(query=query)
        if not company_db:
            raise HTTPException(status_code=404, detail=f"Company id:{company_id} does not exist")

    async def check_for_owner(self, company_id: int):
        query = select(Company).where(Company.company_id == company_id)
        company_db = await self.db.fetch_one(query=query)
        if not company_db:
            raise HTTPException(status_code=404, detail="Company does not exist")
        check_company = CompanyScheme(**dict(company_db))
        if check_company.owner_id != self.current_user_id:
            raise HTTPException(status_code=403, detail="You are not owner in this company")

    async def update_company(self, company_id: int, company: CompanyUpdateRequest) -> ResultCompany:
        await self.check_company_name(company_name=company.company_name)
        query = select(Company).where(Company.company_id == company_id)
        company_db = await self.db.fetch_one(query=query)
        if not company_db:
            raise HTTPException(status_code=404, detail=f"Company id:{company_id} does not exist")
        check_company = CompanyScheme(**dict(company_db))
        if check_company.owner_id != self.current_user_id:
            raise HTTPException(status_code=403, detail="You are not owner in this company")
        update_data = {
            "company_name": company.company_name,
            "company_description": company.company_description,
        }
        query = update(Company).where(Company.company_id == company_id).values(update_data)
        await self.db.execute(query=query)
        updated_company = await self.get_company(company_id=company_id)
        return updated_company

    async def check_company_name(self, company_name: str):
        query = select(Company).where(Company.company_name == company_name)
        company_check = await self.db.fetch_one(query=query)
        if company_check:
            raise HTTPException(status_code=400, detail='Company already exist')

    async def check_current_user(self):
        if not self.current_user_id:
            raise HTTPException(status_code=403, detail="You are not authorized")

    async def check_for_company_existing(self, company_id: int) -> CompanyScheme:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query=query)
        if not company:
            raise HTTPException(status_code=404, detail='Company does not exist')
        return CompanyScheme(**dict(company))

