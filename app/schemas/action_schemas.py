from typing import Optional, TypeVar, Generic
from pydantic import BaseModel


from pydantic.generics import GenericModel
from typing import List

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


class ResponseRequest(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: List[GetInviteRequest] = None


