from pydantic import BaseModel, Field
from uuid import UUID
from driver.model import Driver
from datetime import datetime


class CreateVehicleDTO(BaseModel):
    vehicle_model: str = Field(..., description="The model of the vehicle")
    license_plate: str = Field(..., description="Provide Unique License Plate Number")
    driver: UUID = Field(..., description="Put id (UUID) from a Driver")
    
    
class ResponseVehicleDTO(BaseModel):
    id: UUID
    vehicle_model: str
    license_plate: str
    driver: Driver
    is_active: bool = True
    created_at: datetime
    updated_at: datetime