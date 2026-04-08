from typing import Optional

from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: str
    name: str
    location: str
    capacity: int
    description: str
    amenities: list[str]


class RoomCreate(BaseModel):
    name: str
    location: str
    capacity: int
    description: str = ""
    amenities: list[str] = []


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    amenities: Optional[list[str]] = None
