import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from employee.route import router as employeeRouter
from driver.route import router as driverRouter


load_dotenv()

endpoints = [{
    "method": "GET",
    "regex": r"^\/employee\/all_employee$",
},{
    "method": "POST",
    "regex": r"^\/employee\/create_employee$",
}, {
    "method": "GET",
    "regex": r"^\/driver\/all_driver$",
},{
    "method": "POST",
    "regex": r"^\/driver\/create_driver$",
}, ]


prod = os.environ.get("PRODUCTION", "false")
if prod == "false":
    endpoints += [{
        "method": "GET",
        "regex": r"^\/docs$",
    }, {
        "method": "GET",
        "regex": r"^\/favicon.ico$",
    }, {
        "method": "GET",
        "regex": r"^\/openapi.json$",
    }]


module_api_path = "/api/v1"


def setup(app: FastAPI):
  
    app.include_router(employeeRouter, prefix=module_api_path+"/employee")
    app.include_router(driverRouter, prefix=module_api_path+"/driver")
    
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )

    