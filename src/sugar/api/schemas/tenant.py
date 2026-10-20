import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class TenantRequest(BaseModel):
    company_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


class TenantResponse(BaseModel):
    id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=50)

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
