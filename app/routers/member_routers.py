from fastapi import APIRouter, Depends
from starlette import status

from schemas.action_schemas import Response, AllMembers
from schemas.schemas import UserScheme
from services.member_services import MemberServices
from services.auth_services import get_current_user
from services.company_services import CompanyServices

from db.db_connection import get_db
from databases import Database


member_routers = APIRouter(tags=["actions"])


@member_routers.get('/company/{company_id}/members', response_model=AllMembers, status_code=status.HTTP_200_OK)
async def get_company_members(company_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> AllMembers:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)
    member_service = MemberServices(db=db)
    members_list = await member_service.get_company_members()
    return members_list


@member_routers.delete('/company/{company_id}/member/{member_id}')
async def kick_member_from_company(company_id: int, member_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> AllMembers:

    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)

    member_service = MemberServices(db=db)
    await member_service.validate_member_not_exist(company_id=company_id, member_id=member_id)
    await member_service.kick_member_from_company(company_id=company_id, member_id=member_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="deleted successfully")


@member_routers.delete('/company/{company_id}/leave', response_model=AllMembers, status_code=status.HTTP_200_OK)
async def leave_member_from_company(company_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> AllMembers:

    member_service = MemberServices(db=db, current_user=current_user)
    await member_service.leave_member_from_company(company_id=company_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="deleted successfully")
