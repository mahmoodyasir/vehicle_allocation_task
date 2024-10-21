from fastapi import APIRouter, Request
from driver.model import Driver
from utils import utils
from .model import Vehicle
from .dto import CreateVehicleDTO, ResponseVehicleDTO
from error.exception import EntityNotFoundError
import asyncio
router = APIRouter(tags=["Vehicle"])



@router.post("/create_vehicle", status_code=201)
async def create_vehicle(request: Request, data: CreateVehicleDTO):
    
    try:
        
        license_plate, driver, driver_within_vehicle = await asyncio.gather(
            Vehicle.find_one(Vehicle.license_plate == data.license_plate),
            Driver.find_one(Driver.id == data.driver),
            Vehicle.find_one(Vehicle.driver.id == data.driver)
        )
        
        if license_plate is not None:
            raise Exception("Vehicle with similar licence plate already exists")
        
        if driver is None:
            # raise EntityNotFoundError("No Driver Record Found for the provided UUID")
            return utils.create_response(
                status_code=500,
                success=False,
                message="No Driver Record Found for the provided UUID"
            )
        
        
        if driver_within_vehicle is not None:
            # raise Exception("Same Driver is already assigned to a vehicle. Try another driver UUID")
            return utils.create_response(
                status_code=500,
                success=False,
                message="Same Driver is already assigned to a vehicle. Try another driver UUID"
            )
        
        vehicle_data = data.model_dump(exclude={"driver"})
        vehicle = Vehicle(**vehicle_data, driver=driver)
        
        await vehicle.save()
        
        return utils.create_response(
                status_code=201,
                success=True,
                message="Vehicle has been created successfully",
                data=ResponseVehicleDTO(**vehicle.dict()).model_dump()
        )
        
    except EntityNotFoundError as us:
        return utils.create_response(status_code=us.status_code, success=False, message=us.message)
    
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )
        
        
        
@router.get("/all_vehicle", status_code=200)
async def get_all_vehicle(request: Request):
    
    try:
        
        all_vehicle = await Vehicle.find(fetch_links=True).to_list()
        
        
        return utils.create_response(
                status_code=200,
                success=True,
                message="All Vehicle has been fetched successfully",
                data=[ResponseVehicleDTO(**single_vehicle.dict()) for single_vehicle in all_vehicle]
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )