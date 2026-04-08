from datetime import datetime

from fastapi import HTTPException

from ..models.room import Room
from ..repositories.room_repository import RoomRepository
from ..schemas.room import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    def get_all_rooms(self) -> list[Room]:
        return self.room_repo.find_all()

    def get_room(self, room_id: str) -> Room:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})
        return room

    def create_room(self, data: RoomCreate) -> Room:
        if not data.name.strip():
            raise HTTPException(status_code=400, detail={"error": "스터디룸 이름은 필수입니다."})
        if not data.location.strip():
            raise HTTPException(status_code=400, detail={"error": "위치 정보는 필수입니다."})
        if data.capacity < 1:
            raise HTTPException(status_code=400, detail={"error": "수용 인원은 1명 이상이어야 합니다."})

        if self.room_repo.find_by_name(data.name):
            raise HTTPException(status_code=409, detail={"error": "같은 이름의 스터디룸이 이미 존재합니다."})

        room = Room(
            id=f"room_{int(datetime.now().timestamp() * 1000)}",
            name=data.name,
            location=data.location,
            capacity=data.capacity,
            description=data.description,
            amenities=data.amenities,
        )
        return self.room_repo.save(room)

    def update_room(self, room_id: str, data: RoomUpdate) -> Room:
        room = self.get_room(room_id)

        if data.name is not None:
            if not data.name.strip():
                raise HTTPException(status_code=400, detail={"error": "스터디룸 이름은 필수입니다."})
            if self.room_repo.find_by_name(data.name, exclude_id=room_id):
                raise HTTPException(status_code=409, detail={"error": "같은 이름의 스터디룸이 이미 존재합니다."})
            room.name = data.name

        if data.location is not None:
            if not data.location.strip():
                raise HTTPException(status_code=400, detail={"error": "위치 정보는 필수입니다."})
            room.location = data.location

        if data.capacity is not None:
            if data.capacity < 1:
                raise HTTPException(status_code=400, detail={"error": "수용 인원은 1명 이상이어야 합니다."})
            room.capacity = data.capacity

        if data.description is not None:
            room.description = data.description

        if data.amenities is not None:
            room.amenities = data.amenities

        return self.room_repo.save(room)

    def delete_room(self, room_id: str) -> None:
        room = self.get_room(room_id)
        self.room_repo.delete(room)
