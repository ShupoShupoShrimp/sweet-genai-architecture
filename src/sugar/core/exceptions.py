# ================= PARENT CATEGORY =================
class AppException(Exception):
    pass

# ================= SUBPARENT CATEGORY =================
class NotFoundError(AppException): # 404
    pass

class ConflictError(AppException): # 409
    pass

class AuthenticationError(AppException): # 401
    pass

class AuthorizationError(AppException): # 403
    pass

# ================= CHILD CATEGORY =================
class TenantAlreadyExists(ConflictError):

    def __init__(self, company_name: str):
        self.company = company_name
        super().__init__(
            f"Tenant '{company_name}' already exists"
        )
