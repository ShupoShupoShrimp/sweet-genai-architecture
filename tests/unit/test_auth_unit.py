import pytest
from sugar.core.auth import validate_jwt
from sugar.core.exceptions import ExpiredToken, AudienceMismatch, InsufficientScope


@pytest.mark.asyncio
async def test_expired_jwt_raises_domain_error(make_test_jwt):
    expired_token = make_test_jwt(expires_in=-3600)
    with pytest.raises(ExpiredToken):
        await validate_jwt(expired_token)


@pytest.mark.asyncio
async def test_aud_mismatch_raises_domain_error(make_test_jwt):
    bad_aud_token = make_test_jwt(audience="https://wrong-audience.local")
    with pytest.raises(AudienceMismatch):
        await validate_jwt(bad_aud_token)
