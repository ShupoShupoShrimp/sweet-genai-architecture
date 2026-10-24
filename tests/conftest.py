import time
import pytest
import jwt
from sugar.core.settings import get_settings
import uuid

@pytest.fixture
def make_test_jwt():
    def _generator(
        user_id: uuid.UUID = uuid.UUID("9f8183e6-0d64-40c2-882f-a3e0613f12ac"),
        tenant_id: uuid.UUID = uuid.UUID("792ade83-59e5-4b1f-af2d-3c7236449d61"),
        scope: str = "rag:search",
        audience: str | None = None,
        issuer: str | None = None,
        expires_in: int = 3600,
        kid: str = "test-key-id",
        headers: dict | None = None,
        **kwargs,
    ) -> str:
        
        settings = get_settings()
        now = int(time.time())

        payload = {
            "sub": str(user_id),
            "tenant_id": str(tenant_id),
            "scope": scope,
            "aud": audience or settings.auth_audience,
            "iss": issuer or settings.auth_issuer,
            "iat": now,
            "exp": now + expires_in,
            **kwargs,
        }

        jwt_headers = {"kid": kid}
        if headers:
            jwt_headers.update(headers)

        secret = (
            settings.jwt_secret_key.get_secret_value()
            if settings.jwt_secret_key 
            else "test-secret"
        )

        return jwt.encode(
            payload=payload, 
            key=secret, 
            algorithm="HS256",
            headers=jwt_headers,
        )
    
    return _generator