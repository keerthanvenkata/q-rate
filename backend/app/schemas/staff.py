from pydantic import BaseModel
from typing import Optional
from enum import Enum

class StaffRole(str, Enum):
    MANAGER = "manager"
    WAITER = "waiter"

class StaffBase(BaseModel):
    name: str
    role: StaffRole = StaffRole.WAITER

class StaffCreate(StaffBase):
    pin: str
    cafe_id: int

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[StaffRole] = None
    pin: Optional[str] = None
    is_active: Optional[bool] = None

class StaffResponse(StaffBase):
    id: int
    cafe_id: int
    is_active: bool

    class Config:
        from_attributes = True
