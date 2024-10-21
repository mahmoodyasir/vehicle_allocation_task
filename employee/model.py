from beanie import Document
from base.model import Base



class Employee(Base, Document):
    name: str
    age: int
    position: str