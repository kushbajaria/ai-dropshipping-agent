from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgentJobCreate(BaseModel):
    job_type: str

class AgentJobRead(BaseModel):
    id: int
    job_type: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
