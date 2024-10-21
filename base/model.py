from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = datetime.now(tz=timezone.utc)
    updated_at: datetime = datetime.now(tz=timezone.utc)