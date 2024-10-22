from fastapi import APIRouter, Request
from utils import utils
from .model import Driver
from .dto import DriverDTO, ResponseDriverDTO


router = APIRouter(tags=["Driver"])



@router.get("/all_driver", status_code=200)
async def get_all_driver(request: Request):
    
    try:
        
        # Getting all the driver
        all_driver = await Driver.find().to_list()
        
        
        return utils.create_response(
                status_code=200,
                success=True,
                message="All Driver has been fetched successfully",
                data=[ResponseDriverDTO(**single_driver.dict()) for single_driver in all_driver]
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )
    
    
@router.post("/create_driver", status_code=201)
async def create_driver(request: Request, data: DriverDTO):
    
    try:
        # Creating a Driver Object for later saving it to Driver Collection
        driver = Driver(
            name=data.name,
            age=data.age,
            license_number=data.license_number
        )
    
        await driver.save()
        
        return utils.create_response(
                status_code=201,
                success=True,
                message="Driver has been created successfully",
                data=ResponseDriverDTO(**driver.dict()).model_dump()
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )