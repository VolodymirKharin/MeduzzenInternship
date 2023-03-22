from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CompanyScheme(BaseModel):
    company_id: int
    company_name: str
    company_description: Optional[str] = None
    owner_id: int
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    class Config:
        orm_mode = True


class SignUpCompany(BaseModel):
    company_name: str = Field(..., min_length=4, max_length=20)
    company_description: Optional[str]

    class Config:
        orm_mode = True


class CompanyUpdateRequest(BaseModel):
    company_name: Optional[str]
    company_description: Optional[str]

    class Config:
        orm_mode = True


class CompanyListResponse(BaseModel):
    companies: List[CompanyScheme] = []

    class Config:
        orm_mode = True


class Results(BaseModel):
    result: Optional[CompanyListResponse]

    class Config:
        orm_mode = True


class ResultCompany(BaseModel):
    result: Optional[CompanyScheme]

    class Config:
        orm_mode = True

