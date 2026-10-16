import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sugar.db.models.auth import Tenant
from sugar.db.models.base import Base


class LlmCall(Base):
    __tablename__ = "llm_calls"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="llm_calls")
