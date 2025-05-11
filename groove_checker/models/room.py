from dataclasses import dataclass
from typing import Dict, Any
from groove_checker.config import ROOM_MAP


@dataclass
class RoomAvailabilityDTO:
    name: str             # 필수 (기본값 없음)
    available: bool       # 필수 (기본값 없음)
    available_slots: Dict[str, bool]  # 필수 (기본값 없음)
    total_price: int = 0  # 선택 (기본값 있음)

    @classmethod
    def from_reservation(cls, reservation: 'Reservation', available_slots: Dict[str, bool]):
        start, end = reservation.time.split('-')
        start_hour = int(start.split(':')[0])
        end_hour = int(end.split(':')[0])
        duration = end_hour - start_hour

        return cls(
            name=reservation.room.name,
            available=all(available_slots.values()),
            available_slots=available_slots,
            total_price=reservation.room.price * duration
        )

    def to_dict(self):
        return {
            "name": self.name,
            "available": self.available,
            "available_slots": self.available_slots,
            "total_price": self.total_price
        }


@dataclass
class Room:
    """연습실 정보"""
    name: str
    price: int

    @classmethod
    def from_id(cls, room_id: str):
        if room_id not in ROOM_MAP:
            raise ValueError(f"Invalid room_id: {room_id}")
        info = ROOM_MAP[room_id]
        return cls(name=info["name"], price=info["price"])

@dataclass
class Reservation:
    room: Room
    time: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "room": self.room.name,
            "time": self.time,
            "price": self.room.price
        }

