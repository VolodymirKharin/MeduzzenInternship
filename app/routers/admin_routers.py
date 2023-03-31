from fastapi import APIRouter, Depends
from starlette import status


from schemas.user_schemas import UserScheme
from schemas.admin_schemas import AdminId, ResponseAddAdmin, ResponseAdminsList

from services.admin_services import AdminServices
from services.auth_services import get_current_user
from services.company_services import CompanyServices

from db.db_connection import get_db
from databases import Database


admin_routers = APIRouter(tags=["admins"])


@admin_routers.post('/company/{company_id}/admin', response_model=ResponseAddAdmin, status_code=status.HTTP_201_CREATED)
async def create_company_admin(company_id: int, user: AdminId, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> ResponseAddAdmin:

    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)

    admin_service = AdminServices(db=db, current_user=current_user)
    await admin_service.validate_user_not_exist(company_id=company_id, user_id=user.user_id)


    updated_member = await admin_service.create_company_admin(company_id=company_id, user_id=user.user_id)

    return ResponseAddAdmin(
        status_code=status.HTTP_201_CREATED,
        detail="success",
        result=updated_member)



@admin_routers.get('/company/{company_id}/admins', response_model=ResponseAdminsList, status_code=status.HTTP_200_OK)
async def get_company_admins(company_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> ResponseAdminsList:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)

    admin_service = AdminServices(db=db, current_user=current_user)

    admins = await admin_service.get_company_admins(company_id=company_id)

    return ResponseAdminsList(
        status_code=status.HTTP_200_OK,
        detail="success",
        result=admins)


@admin_routers.delete('/company/{company_id}/admin/{user_id}', response_model=ResponseAddAdmin, status_code=status.HTTP_200_OK)
async def delete_company_admin(company_id: int, user_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> ResponseAddAdmin:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)
    admin_service = AdminServices(db=db, current_user=current_user)
    await admin_service.check_for_user_exist(company_id=company_id, user_id=user_id)
    await admin_service.delete_company_admin(company_id=company_id, user_id=user_id)

    return ResponseAddAdmin(
        status_code=status.HTTP_200_OK,
        detail="success",
        )