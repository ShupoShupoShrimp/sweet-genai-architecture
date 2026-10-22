from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from typing import Any

import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from sugar.core.exceptions import (
    AudienceMismatch,
    ExpiredToken,
    InsufficientScope,
    InvalidApiKey,
    InvalidToken,
    RevokedApiKey,
)
from sugar.core.settings import get_settings
from sugar.db.models.auth import ApiKey


async def create_api_key(
    session: AsyncSession,
    tenant_id: uuid.UUID,
) -> tuple[ApiKey, str]:
    raw_key = f"sk_live_{secrets.token_urlsafe(32)}"

    hashed_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    new_api_key = ApiKey(tenant_id=tenant_id, key_hash=hashed_key)

    session.add(new_api_key)
    await session.commit()
    await session.refresh(new_api_key)

    return new_api_key, raw_key


async def validate_api_keys(
    tenant_id: uuid.UUID,
    raw_api_key: str,
    session: AsyncSession,
) -> Any:
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


async def validate_jwt(
    jwt_token: str,
    required_scope: str | None = None,
    jwks_client: jwt.PyJWKClient | None = None,
) -> dict[str, Any]:
    settings = get_settings()

    if settings.jwt_algorithm == "HS256":
        if not settings.jwt_secret_key:
            raise InvalidToken("secret key not configured")
        secret_key = settings.jwt_secret_key.get_secret_value()
    else:
        header = jwt.get_unverified_header(jwt_token)
        key_id = header.get("kid")
        if not key_id:
            raise InvalidToken("The token is missing the 'key id', therefore it is invalid")

        if jwks_client:
            try:
                secret_key = jwks_client.get_signing_key_from_jwt(jwt_token).key
            except Exception as e:
                raise InvalidToken(f"JWKS check up failed: {e}") from e

        else:
            raise InvalidToken("Needed JWKS client for checkcup")

    try:
        payload = jwt.decode(
            jwt=jwt_token,
            key=secret_key,
            algorithms=[settings.jwt_algorithm],
            audience=settings.auth_audience,
            issuer=settings.auth_issuer,
            options={"require": ["sub", "tenant_id", "exp"]},
        )

    except jwt.ExpiredSignatureError:
        raise ExpiredToken() from None
    except jwt.InvalidAudienceError:
        raise AudienceMismatch() from None
    except jwt.PyJWTError as exc:
        raise InvalidToken(f"JWT validation failed: {exc}") from exc

    tenant_id_claim = payload.get("tenant_id")

    if isinstance(tenant_id_claim, str):
        raise InvalidToken("Mising or invalid tenant_id claim")

    try:
        tenant_id = uuid.UUID(tenant_id_claim)
    except ValueError:
        raise InvalidToken("Invalid tenant_id format") from None

    token_scope = payload.get("scope", "").split()

    if required_scope and required_scope not in token_scope:
        raise InsufficientScope(required_scope=required_scope)

    return {
        "user_id": payload.get("sub"),
        "tenant_id": tenant_id,
        "scopes": token_scope,
    }
