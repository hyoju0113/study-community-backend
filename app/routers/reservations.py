from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from ..repositories.room_repository import RoomRepository
from ..repositories.reservation_repository import ReservationRepository
from ..services.reservation_service import ReservationService
from ..schemas.reservation import ReservationCreate

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: Session = Depends(get_db)) -> ReservationService:
    return ReservationService(ReservationRepository(db), RoomRepository(db))


@router.post("", status_code=201)
def create_reservation(
    data: ReservationCreate,
    service: ReservationService = Depends(get_reservation_service),
    current_user=Depends(get_current_user),
):
    reservation = service.create_reservation(data, current_user)
    return {
        "id": reservation.id,
        "roomId": reservation.room_id,
        "date": reservation.date,
        "startTime": reservation.start_time,
        "endTime": reservation.end_time,
        "purpose": reservation.purpose,
        "userId": current_user.id,
        "username": current_user.username,
        "createdAt": reservation.created_at.isoformat(),
    }


@router.get("/me")
def get_my_reservations(
    service: ReservationService = Depends(get_reservation_service),
    current_user=Depends(get_current_user),
):
    items = service.get_my_reservations(current_user.id)
    return [
        {
            "id": item["reservation"].id,
            "roomId": item["reservation"].room_id,
            "roomName": item["room_name"],
            "date": item["reservation"].date,
            "startTime": item["reservation"].start_time,
            "endTime": item["reservation"].end_time,
            "purpose": item["reservation"].purpose,
            "userId": current_user.id,
            "username": current_user.username,
            "createdAt": item["reservation"].created_at.isoformat(),
        }
        for item in items
    ]


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: str,
    service: ReservationService = Depends(get_reservation_service),
    current_user=Depends(get_current_user),
):
    service.cancel_reservation(reservation_id, current_user)
    return {"message": "예약이 취소되었습니다."}
