from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sugar.core.exceptions import TenantAlreadyExists
from sugar.db.models.auth import Tenant


async def register_tenant(
    company_name: str,
    session: AsyncSession,
) -> Tenant:

    stmt = select(Tenant).where(Tenant.name == company_name)
    result = await session.execute(stmt)
    tenant = result.scalar_one_or_none()

    if tenant is not None:
        raise TenantAlreadyExists(company_name=company_name)

    new_tenant = Tenant(name=company_name)

    session.add(new_tenant)
    await session.commit()
    await session.refresh(new_tenant)

    return new_tenant
