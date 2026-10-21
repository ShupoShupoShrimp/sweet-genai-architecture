from __future__ import annotations

import hashlib
import hmac
from sugar.db.models.auth import ApiKey
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sugar.core.exceptions import InvalidApiKey, RevokedApiKey
import uuid


async def validate_api_keys(
    tenant_id: uuid.UUID,
    raw_api_key: str,
    session: AsyncSession,
):
    hashed_raw_key = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()

    stmt = select(ApiKey).options(selectinload(ApiKey.tenant)).where(ApiKey.tenant_id == tenant_id)

    result = await session.execute(stmt)

    api_key_records = result.scalars().all()

    for api_key_record in api_key_records:
        if hmac.compare_digest(hashed_raw_key, api_key_record.key_hash):
            if api_key_record.revoked_at is not None:
                raise RevokedApiKey()
            return api_key_record.tenant

    raise InvalidApiKey()
