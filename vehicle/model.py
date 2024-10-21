from beanie import Document, Link
from base.model import Base
from driver.model import Driver


class Vehicle(Base, Document):
    vehicle_model: str
    license_plate: str
    driver: Link[Driver]