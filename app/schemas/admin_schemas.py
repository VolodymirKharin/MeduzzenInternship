from schemas.action_schemas import Member


from typing import Optional, TypeVar, Generic
from pydantic import BaseModel


from pydantic.generics import GenericModel
from typing import List


Model = TypeVar("Model")

class AdminId(BaseModel):
    user_id: int


class ResponseAddAdmin(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: Optional[Member] = None


class AdminsList(BaseModel):
    admins: List[Member] = []

class ResultAdminsList(BaseModel):
    result: Optional[AdminsList]

class ResponseAdminsList(GenericModel, Generic[Model]):
    status_code: int
    detail: str
    result: Optional[AdminsList]