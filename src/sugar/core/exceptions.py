# ================= PARENT CATEGORY =================
class AppException(Exception):
    """Base exception for application-wide domain errors."""

    pass


class JSONWebTokenException(Exception):
    """Base exception for all JWT operations."""

    pass


# ================= SUBPARENT CATEGORY =================


# === Tenant Subparent category ===
class NotFoundError(AppException):  # 404
    pass


class ConflictError(AppException):  # 409
    pass


class AuthenticationError(AppException):  # 401
    pass


class AuthorizationError(AppException):  # 403
    pass


# ===== JSONWebToken Subparent category =====
class ExpiredSignatureError(JSONWebTokenException):
    pass


class InvalidAudienceError(JSONWebTokenException):
    pass


class JWTError(JSONWebTokenException):
    pass


# ================= CHILD CATEGORY =================


# =========== Tenant ===========
class TenantAlreadyExists(ConflictError):  # 409
    def __init__(self, company_name: str):
        self.company = company_name
        super().__init__(f"Tenant '{company_name}' already exists.")


# =========== ApiKey ===========
class InvalidApiKey(AuthenticationError):  # 401
    def __init__(self):
        super().__init__("The ApiKey is Invalid.")


class RevokedApiKey(AuthenticationError):  # 401
    def __init__(self):
        super().__init__("The ApiKey was revoked. Therefore it is unavailable.")


# =========== JSON Web Token ===========
class AudienceMismatch(AuthenticationError, InvalidAudienceError):  # 401
    def __init__(self, message: str = "Token audience (aud) mismatch."):
        super().__init__(message)


class ExpiredToken(AuthenticationError, ExpiredSignatureError):  # 401
    def __init__(self, message: str = "The token has expired."):
        super().__init__(message)


class InsufficientScope(AuthorizationError):  # 403
    def __init__(self, required_scope: str):
        self.required_scope = required_scope
        super().__init__(f"Missing required scope: '{required_scope}'.")


class InvalidToken(AuthenticationError, JWTError):  # 401
    def __init__(self, message: str = "The token is invalid."):
        super().__init__(message)
