from beanie import Document
from base.model import Base


class Driver(Base, Document):
    name: str
    age: int
    license_number: str