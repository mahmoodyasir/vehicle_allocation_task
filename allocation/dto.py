from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from employee.model import Employee
from vehicle.dto import ResponseVehicleDTO
from vehicle.model import Vehicle


class CreateAllocationDTO(BaseModel):
    employee: UUID = Field(..., description="Employee UUID")
    vehicle: UUID = Field(..., description="Vehicle UUID")
    allocation_date: date = Field(..., description="Date of allocation")


class UpdateAllocationDTO(BaseModel):
    employee: UUID = Field(None, description="Employee UUID")
    vehicle: UUID = Field(None, description="Vehicle UUID")
    allocation_date: date = Field(None, description="Date of allocation")


class ResponseAllocationDTO(BaseModel):
    id: UUID
    employee: Employee
    vehicle: ResponseVehicleDTO
    allocation_date: date
    created_at: datetime
    updated_at: datetime