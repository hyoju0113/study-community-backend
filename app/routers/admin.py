from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_admin_user
from ..repositories.room_repository import RoomRepository
from ..services.room_service import RoomService
from ..schemas.room import RoomCreate, RoomUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    return RoomService(RoomRepository(db))


@router.post("/rooms", status_code=201)
def create_room(
    data: RoomCreate,
    service: RoomService = Depends(get_room_service),
    admin=Depends(get_admin_user),
):
    room = service.create_room(data)
    return {
        "id": room.id,
        "name": room.name,
        "location": room.location,
        "capacity": room.capacity,
        "description": room.description,
        "amenities": room.amenities or [],
    }


@router.put("/rooms/{room_id}")
def update_room(
    room_id: str,
    data: RoomUpdate,
    service: RoomService = Depends(get_room_service),
    admin=Depends(get_admin_user),
):
    room = service.update_room(room_id, data)
    return {
        "id": room.id,
        "name": room.name,
        "location": room.location,
        "capacity": room.capacity,
        "description": room.description,
        "amenities": room.amenities or [],
    }


@router.delete("/rooms/{room_id}")
def delete_room(
    room_id: str,
    service: RoomService = Depends(get_room_service),
    admin=Depends(get_admin_user),
):
    service.delete_room(room_id)
    return {"message": "스터디룸이 삭제되었습니다."}
