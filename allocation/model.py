from beanie import Document, Link
from base.model import Base
from employee.model import Employee
from vehicle.model import Vehicle
from datetime import date


class Allocation(Base, Document):
    employee: Link[Employee]
    vehicle: Link[Vehicle]
    allocation_date: date