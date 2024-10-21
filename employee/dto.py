from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class EmployeeDTO(BaseModel):
    name: str
    age: int
    position: str
    
class ResponseEmployeeDTO(BaseModel):
    id: UUID
    name: str
    age: int
    position: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime