from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AgentJob(Base):
    __tablename__ = "agent_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    input_payload: Mapped[dict] = mapped_column(JSON)
    result_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
