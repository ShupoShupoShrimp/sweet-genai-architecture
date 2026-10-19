from pydantic import BaseModel, StringConstraints, ConfigDict
import uuid

class PostApiKey(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    raw_api_key: str

