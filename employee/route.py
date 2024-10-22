from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from utils import utils

from .model import Employee

from .dto import EmployeeDTO, ResponseEmployeeDTO


router = APIRouter(tags=["Employee"])



@router.get("/all_employee", status_code=200)
async def get_all_employee(request: Request):
    
    try:
        # Getting all employee
        all_employee = await Employee.find().to_list()
        
        
        return utils.create_response(
                status_code=200,
                success=True,
                message="All Employee has been fetched successfully",
                data=[ResponseEmployeeDTO(**single_employee.dict()) for single_employee in all_employee]
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )
    
    
@router.post("/create_employee", status_code=201)
async def create_employee(request: Request, data: EmployeeDTO):
    
    try:
        # Creating a Employee Object for later saving it to Employee Collection
        employee = Employee(
            name=data.name,
            age=data.age,
            position=data.position
        )
    
        await employee.save()
        
        return utils.create_response(
                status_code=201,
                success=True,
                message="Employee has been created successfully",
                data=ResponseEmployeeDTO(**employee.dict()).model_dump()
        )
    except Exception as e:
        return utils.create_response(
            status_code=500,
            success=False,
            message=str(e)
        )