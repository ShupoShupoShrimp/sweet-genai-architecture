from fastapi import APIRouter, Depends, status
from sugar.core.tenant import register_tenant, create_api_key
from sqlalchemy.ext.asyncio import AsyncSession
from sugar.db.session import get_db
from sugar.api.schemas.tenant import TenantRequest, TenantResponse
from sugar.api.schemas.api_key import PostApiKey
import uuid

router = APIRouter(prefix="/v1/admin", tags=["Admin Provisioning"])


@router.post(
    "/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    body: TenantRequest,
    session: AsyncSession = Depends(get_db),
):
    tenant = await register_tenant(company_name=body.company_name, session=session)

    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        created_at=tenant.created_at,
    )


@router.post(
    "/tenants/{tenant_id}/keys",
    response_model=PostApiKey,
    status_code=status.HTTP_201_CREATED,
)
async def create_key(
    tenant_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    api_key, raw_key = await create_api_key(session=session, tenant_id=tenant_id)

    return PostApiKey(
        id=api_key.id,
        tenant_id=api_key.tenant_id,
        raw_api_key=raw_key,
    )
