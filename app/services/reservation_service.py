from datetime import datetime, date

from fastapi import HTTPException

from ..models.reservation import Reservation
from ..models.user import User
from ..repositories.reservation_repository import ReservationRepository
from ..repositories.room_repository import RoomRepository
from ..schemas.reservation import ReservationCreate


class ReservationService:
    def __init__(self, reservation_repo: ReservationRepository, room_repo: RoomRepository):
        self.reservation_repo = reservation_repo
        self.room_repo = room_repo

    def get_room_reservations(self, room_id: str, reservation_date: str) -> list[dict]:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})

        return self.reservation_repo.find_by_room_and_date(room_id, reservation_date)

    def create_reservation(self, data: ReservationCreate, current_user: User) -> Reservation:
        room = self.room_repo.find_by_id(data.roomId)
        if not room:
            raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})

        if not data.purpose.strip():
            raise HTTPException(status_code=400, detail={"error": "예약 목적은 필수입니다."})

        if data.startTime >= data.endTime:
            raise HTTPException(status_code=400, detail={"error": "시작 시간은 종료 시간보다 빨라야 합니다."})

        if data.startTime < "09:00" or data.endTime > "22:00":
            raise HTTPException(status_code=400, detail={"error": "예약 가능 시간은 09:00~22:00입니다."})

        reservation_date = datetime.strptime(data.date, "%Y-%m-%d").date()
        if reservation_date < date.today():
            raise HTTPException(status_code=400, detail={"error": "과거 날짜에는 예약할 수 없습니다."})

        if self.reservation_repo.find_conflicting(data.roomId, data.date, data.startTime, data.endTime):
            raise HTTPException(status_code=409, detail={"error": "해당 시간대에 이미 예약이 존재합니다."})

        reservation = Reservation(
            id=f"rsv_{int(datetime.now().timestamp() * 1000)}",
            room_id=data.roomId,
            user_id=current_user.id,
            date=data.date,
            start_time=data.startTime,
            end_time=data.endTime,
            purpose=data.purpose,
        )
        return self.reservation_repo.save(reservation)

    def get_my_reservations(self, user_id: str) -> list[dict]:
        reservations = self.reservation_repo.find_by_user(user_id)
        result = []
        for r in reservations:
            room = self.room_repo.find_by_id(r.room_id)
            result.append({"reservation": r, "room_name": room.name if room else "알 수 없음"})
        return result

    def cancel_reservation(self, reservation_id: str, current_user: User) -> None:
        reservation = self.reservation_repo.find_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail={"error": "예약을 찾을 수 없습니다."})

        if reservation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail={"error": "본인의 예약만 취소할 수 있습니다."})

        self.reservation_repo.delete(reservation)
