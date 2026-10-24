from sugar.api.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app=app)

def test_auth_401():
    """Missing Bearer header returns 401."""
    response = client.get("/api/v1/protected")
    assert response.status_code == 401

def test_wrong_scope_403(make_test_jwt):
    """Token missing required scope returns 403."""
    token = make_test_jwt(scope="other:reader")

    response = client.get(
        "/v1/protected", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

def test_expired_token_401(make_test_jwt):
    """Expired Token returns 401."""
    expired_token = make_test_jwt(eexpires_in=-3600)

    response = client.get(
        "/v1/protected",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401

def aud_mismatch_401(make_test_jwt):
    """Audience mismatch returns 401."""
    wrong_audience_token = make_test_jwt(audience="https://wrong_company.com")

    response = client.get(
        "/v1/protected",
        headers={"Authorization": f"Bearer {wrong_audience_token}"}
    )

    assert response.status_code == 401
