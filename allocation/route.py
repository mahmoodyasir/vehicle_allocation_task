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
from fastapi import Query


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
        

@router.delete("/delete_allocation/{allocation_id}", status_code=200)
async def delete_allocation(allocation_id: UUID):
    try:
        allocation = await Allocation.get(allocation_id, fetch_links=True)
        if not allocation:
            raise Exception("Allocation not found.")


        if allocation.allocation_date < date.today():
            raise Exception("Cannot delete an allocation after the allocation date.")


        await allocation.delete()

        return utils.create_response(
            status_code=200,
            success=True,
            message="Allocation deleted successfully",
            data=ResponseAllocationDTO(**allocation.dict()).model_dump()
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )
        
        

@router.get("/allocation_history", status_code=200, description="If All The Params Are Empty, Then It Will GET All Existing Data of ALLOCATION")
async def allocation_history(
    employee_id: UUID | None = Query(None, description="Filter by employee ID (UUID),  Example: aff4e786-01e3-4b30-a26f-427ce22bfda0"),
    vehicle_id: UUID | None = Query(None, description="Filter by vehicle ID (UUID),  Example: ee0be214-dea0-4d29-8656-6a83d207304d"),
    start_date: date | None = Query(None, description="Filter allocations from this date (YYYY-MM-DD),  Example: 2024-10-21"),
    end_date: date | None = Query(None, description="Filter allocations up to this date (YYYY-MM-DD),  Example: 2024-10-27"),
):
    try:
        
        query_filters = {}

        if employee_id:
            query_filters["employee._id"] = employee_id
        
        if vehicle_id:
            query_filters["vehicle._id"] = vehicle_id

        if start_date:
            query_filters["allocation_date"] = {"$gte": start_date}
        
        if end_date:
            if "allocation_date" in query_filters:
                query_filters["allocation_date"]["$lte"] = end_date
            else:
                query_filters["allocation_date"] = {"$lte": end_date}

   
        allocations = await Allocation.find_many(query_filters, fetch_links=True).to_list()


        if not allocations:
            return utils.create_response(
                status_code=404,
                success=False,
                message="No allocations found with the provided filters."
            )

        allocation_reports = [ResponseAllocationDTO(**allocation.dict()) for allocation in allocations]
        

        return utils.create_response(
            status_code=200,
            success=True,
            message="Allocation history retrieved successfully.",
            data=allocation_reports
        )
    
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )