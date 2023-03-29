from typing import Optional, List, TypeVar,Generic
from pydantic import BaseModel, Field


from pydantic.generics import GenericModel
from typing import List
from datetime import datetime

Model = TypeVar("Model")


class GetInviteRequest(BaseModel):
    action_id: int
    user_id: int
    company_id: int
    action_type: str


class SendInviteRequest(BaseModel):
    user_id: int
    company_id: int

    class Config:
        orm_mode = True





class Response(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: Optional[GetInviteRequest] = None

class AllUserInvites(BaseModel):
    result: List[SendInviteRequest]

class AllCompanyInvites(BaseModel):
    result: List[SendInviteRequest]

class Member(BaseModel):
    member_id: int
    user_id: int
    company_id: int
    user_role: str
class ResponseMember(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: Optional[Member] = None


class MemberListResponse(BaseModel):
    users: List[Member] = []
class AllMembers(BaseModel):
    result: Optional[MemberListResponse]




class SendRequest(BaseModel):
    company_id: int

    class Config:
        orm_mode = True


class AllUserRequest(BaseModel):
    result: List[GetInviteRequest]


# class RequestsList(BaseModel):
#     requests: List[GetInviteRequest]
class ResponseRequest(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: List[GetInviteRequest] = None



# class RequestListResponse(BaseModel):
#     users: List[Member] = []
# class AllRequests(BaseModel):
#     result: Optional[RequestListResponse]

# class Response(BaseModel):
#     status_code: int = 200
#     detail: str = None
# #    result: Optional[SendInviteRequest]


# class Response(BaseModel):
#     result: Optional[SendInviteRequest]

# class SignUpCompany(BaseModel):
#     company_name: str = Field(..., min_length=4, max_length=20)
#     company_description: Optional[str]
#
#     class Config:
#         orm_mode = True
#
#
# class CompanyUpdateRequest(BaseModel):
#     company_name: Optional[str]
#     company_description: Optional[str]
#
#     class Config:
#         orm_mode = True
#
#
# class CompanyListResponse(BaseModel):
#     companies: List[CompanyScheme] = []
#
#     class Config:
#         orm_mode = True
#
#

# class ResultInviteRequest(BaseModel):
#     result: Optional[SendInviteRequest]


# class Results(BaseModel):
#     result: Optional[CompanyListResponse]
#
#     class Config:
#         orm_mode = True
#
#
# class ResultCompany(BaseModel):
#     result: Optional[CompanyScheme]
#
#     class Config:
#         orm_mode = True

