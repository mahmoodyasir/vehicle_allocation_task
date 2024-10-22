import asyncio
from uuid import UUID
from fastapi import APIRouter
from datetime import date
from utils import utils
from vehicle.dto import ResponseVehicleDTO
from .dto import CreateAllocationDTO, UpdateAllocationDTO, ResponseAllocationDTO
from .model import Allocation
from vehicle.model import Vehicle
from employee.model import Employee


router = APIRouter(tags=["Allocation"])



@router.post("/create_allocation", status_code=201)
async def create_allocation(data: CreateAllocationDTO):
    try:
        if data.allocation_date < date.today():
            raise Exception("Cannot create an allocation with a past date.")
        
        employee, vehicle, existing_allocation = await asyncio.gather(
            Employee.get(data.employee),
            Vehicle.get(data.vehicle, fetch_links=True),
            Allocation.find_one(Allocation.vehicle.id == data.vehicle, Allocation.allocation_date == data.allocation_date)
        )
        
        if existing_allocation is not None:
            raise Exception(f"Vehicle is already allocated to another employee at this day {data.allocation_date} .")
        
        if not employee:
            raise Exception("Employee not found.")
        
        if not vehicle:
            raise Exception("Vehicle not found.")
        
        
        allocation_data = data.model_dump(exclude={"employee", "vehicle"})
        allocation = Allocation(**allocation_data, employee=employee, vehicle=vehicle)
        
        
        await allocation.save()
        
        
        return utils.create_response(
            status_code=201,
            success=True,
            message="Allocation created successfully",
            data=ResponseAllocationDTO(**allocation.dict()).model_dump()
        )
    
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )



@router.patch("/update_allocation/{allocation_id}", status_code=200)
async def update_allocation(allocation_id: UUID, data: UpdateAllocationDTO):
    try:
        allocation = await Allocation.get(allocation_id, fetch_links=True)
        if not allocation:
            raise Exception("Allocation not found.")

        if allocation.allocation_date < date.today():
            raise Exception("Cannot update an allocation after the allocation date.")

        update_data = data.model_dump(exclude_unset=True)

        if "employee" in update_data:
            employee = await Employee.get(update_data["employee"])
            if not employee:
                raise Exception("Employee not found.")
            allocation.employee = employee
            
        if "allocation_date" in update_data:
            if update_data["allocation_date"] < date.today():
                raise Exception("Cannot set an allocation date in the past.")
            allocation.allocation_date = update_data["allocation_date"]
            

        if "vehicle" in update_data:
            vehicle = await Vehicle.get(update_data["vehicle"], fetch_links=True)
            if not vehicle:
                raise Exception("Vehicle not found.")
            
            existing_allocation = await Allocation.find_one(
                Allocation.vehicle.id == update_data["vehicle"],
                Allocation.allocation_date == update_data["allocation_date"],
                Allocation.id != allocation.id
            )
            
            if existing_allocation:
                raise Exception(f"Vehicle is already allocated to another employee on {allocation.allocation_date}.")
            allocation.vehicle = vehicle
            

        
        await allocation.save()

        return utils.create_response(
            status_code=200,
            success=True,
            message="Allocation updated successfully",
            data=ResponseAllocationDTO(**allocation.dict()).model_dump()
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )