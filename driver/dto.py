from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class DriverDTO(BaseModel):
    name: str
    age: int
    license_number: str
    
    
class ResponseDriverDTO(BaseModel):
    id: UUID
    name: str
    age: int
    license_number: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime