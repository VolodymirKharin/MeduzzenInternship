from fastapi import APIRouter, Depends
from starlette import status

from schemas.action_schemas import Response, Member, GetInviteRequest, ResponseRequest, SendRequest, AllUserRequest, ResponseMember
from schemas.user_schemas import UserScheme

from services.invite_services import InviteServices
from services.request_services import RequestServices
from services.auth_services import get_current_user
from services.company_services import CompanyServices

from db.db_connection import get_db
from databases import Database


request_routers = APIRouter(tags=["request"])


@request_routers.post("/request", response_model=Response[GetInviteRequest], status_code=status.HTTP_201_CREATED)
async def send_request(request: SendRequest, current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> Response[GetInviteRequest]:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_company_for_exist(company_id=request.company_id)

    request_service = RequestServices(db=db, current_user=current_user)

    await request_service.check_for_exist_member(company_id=request.company_id)
    await request_service.check_for_owner(company_id=request.company_id)

    await request_service.check_for_owner(company_id=request.company_id)
    new_request = await request_service.send_request(request=request)
    return Response(
        status_code=status.HTTP_201_CREATED,
        detail="success",
        result=new_request
    )


@request_routers.get("/request/my", response_model=AllUserRequest, status_code=status.HTTP_200_OK)
async def get_user_request(current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> AllUserRequest:
    request_service = RequestServices(db=db, current_user=current_user)
    my_invites = await request_service.get_my_request()
    return AllUserRequest(result=my_invites.result)


@request_routers.get("/request/company/{company_id}", response_model=ResponseRequest)
async def get_company_request(company_id: int, current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> ResponseRequest:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)

    request_service = RequestServices(db=db, current_user=current_user)
    company_request = await request_service.get_company_request(company_id=company_id)
    return ResponseRequest(
        status_code=status.HTTP_200_OK,
        detail="success",
        result=company_request
    )


@request_routers.delete('/request/{request_id}', response_model=Response[Member], status_code=status.HTTP_200_OK)
async def user_cancel_request(request_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> Response[Member]:

    action_service = InviteServices(db=db, current_user=current_user)
    request = await action_service.check_action_for_exist(action_id=request_id)

    request_service = RequestServices(db=db, current_user=current_user)
    await request_service.company_cancel_request(request=request)
    return Response(
        status_code=200,
        detail="success",
    )


@request_routers.get('/request/{request_id}/accept', response_model=ResponseMember[Member], status_code=status.HTTP_200_OK)
async def company_accept_request(request_id: int, db: Database = Depends(get_db),
                                current_user: UserScheme = Depends(get_current_user)) -> ResponseMember[Member]:

    action_service = InviteServices(db=db, current_user=current_user)
    request = await action_service.check_action_for_exist(action_id=request_id)

    request_service = RequestServices(db=db, current_user=current_user)
    await request_service.check_not_owner(company_id=request.company_id, message="accept")

    new_member = await request_service.company_accept_request(request=request)

    return ResponseMember(
        status_code=200,
        detail="success",
        result=new_member
    )


@request_routers.get('/request/{request_id}/decline', response_model=Response[Member], status_code=status.HTTP_200_OK)
async def company_decline_request(request_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> Response[Member]:

    action_service = InviteServices(db=db, current_user=current_user)
    request = await action_service.check_action_for_exist(action_id=request_id)

    request_service = RequestServices(db=db, current_user=current_user)
    await request_service.check_not_owner(company_id=request.company_id, message="decline")

    await request_service.company_decline_request(request=request)
    return Response(
        status_code=200,
        detail="success",
    )
