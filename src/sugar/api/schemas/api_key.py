from pydantic import BaseModel, StringConstraints, ConfigDict
import uuid
import datetime
from typing import Optional, Annotated

KeyHash = Annotated[str, StringConstraints(pattern=r"^[a-fA-0-F9]{64}$", to_lower=True)]


class ApiKeyResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID

    key_hash: KeyHash
    created_at: datetime.datetime
    revoked_at: Optional[datetime.datetime]

    model_config = ConfigDict(from_attributes=True)