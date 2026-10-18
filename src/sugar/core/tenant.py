from sqlalchemy.ext.asyncio import AsyncSession
from sugar.db.models.auth import Tenant, ApiKey
import secrets
import hashlib


async def register_tenant(
    company_name: str,
    session: AsyncSession,
) -> Tenant:

    new_tenant = Tenant(name=company_name)

    session.add(new_tenant)
    await session.commit()
    await session.refresh(new_tenant)

    return new_tenant


async def create_api_key(
    session: AsyncSession,
    tenant_id,
    ) -> tuple[ApiKey, str]:
    raw_key = f"sk_live_{secrets.token_urlsafe(32)}"

    hashed_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    new_api_key = ApiKey(tenant_id=tenant_id, key_hash=hashed_key)

    session.add(new_api_key)
    await session.commit()
    await session.refresh(new_api_key)

    return new_api_key, raw_key