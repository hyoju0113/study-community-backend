from sqlalchemy.orm import Session

from ..models.room import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def find_by_id(self, room_id: str) -> Room | None:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def find_by_name(self, name: str, exclude_id: str | None = None) -> Room | None:
        query = self.db.query(Room).filter(Room.name == name)
        if exclude_id:
            query = query.filter(Room.id != exclude_id)
        return query.first()

    def save(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room: Room) -> None:
        self.db.delete(room)
        self.db.commit()
