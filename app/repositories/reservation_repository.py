from sqlalchemy.orm import Session

from ..models.reservation import Reservation


class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_room_and_date(self, room_id: str, date: str) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.room_id == room_id, Reservation.date == date)
            .order_by(Reservation.start_time)
            .all()
        )

    def find_by_user(self, user_id: str) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.user_id == user_id)
            .order_by(Reservation.date, Reservation.start_time)
            .all()
        )

    def find_by_id(self, reservation_id: str) -> Reservation | None:
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def find_conflicting(self, room_id: str, date: str, start_time: str, end_time: str) -> Reservation | None:
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.room_id == room_id,
                Reservation.date == date,
                Reservation.start_time < end_time,
                Reservation.end_time > start_time,
            )
            .first()
        )

    def save(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def delete(self, reservation: Reservation) -> None:
        self.db.delete(reservation)
        self.db.commit()
