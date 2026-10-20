import uuid

from pydantic import BaseModel


class PostApiKey(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    raw_api_key: str
