from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..repositories.room_repository import RoomRepository
from ..repositories.reservation_repository import ReservationRepository
from ..services.reservation_service import ReservationService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("")
def get_rooms(db: Session = Depends(get_db)):
    room_repo = RoomRepository(db)
    rooms = room_repo.find_all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "capacity": r.capacity,
            "description": r.description,
            "amenities": r.amenities or [],
        }
        for r in rooms
    ]


@router.get("/{room_id}")
def get_room(room_id: str, db: Session = Depends(get_db)):
    from ..services.room_service import RoomService
    service = RoomService(RoomRepository(db))
    room = service.get_room(room_id)
    return {
        "id": room.id,
        "name": room.name,
        "location": room.location,
        "capacity": room.capacity,
        "description": room.description,
        "amenities": room.amenities or [],
    }


@router.get("/{room_id}/reservations")
def get_room_reservations(
    room_id: str,
    date: str = Query(..., description="조회할 날짜 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    room_repo = RoomRepository(db)
    reservation_repo = ReservationRepository(db)
    service = ReservationService(reservation_repo, room_repo)
    reservations = service.get_room_reservations(room_id, date)

    result = []
    for r in reservations:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append({
            "id": r.id,
            "roomId": r.room_id,
            "date": r.date,
            "startTime": r.start_time,
            "endTime": r.end_time,
            "purpose": r.purpose,
            "userId": r.user_id,
            "username": user.username if user else "알 수 없음",
            "createdAt": r.created_at.isoformat(),
        })
    return result
