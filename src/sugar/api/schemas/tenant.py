from pydantic import BaseModel, Field
import datetime
import uuid


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

    class Config:
        from_attributes: True
