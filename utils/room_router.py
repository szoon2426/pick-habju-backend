from typing import Literal
from models.dto import RoomKey

RoomType = Literal["dream", "groove", "naver"]


def get_room_type(business_id: str) -> RoomType:
    if business_id == "dream_sadang":
        return "dream"
    elif business_id == "sadang":
        return "groove"
    return "naver"


def filter_rooms_by_type(rooms: list[RoomKey], target_type: RoomType) -> list[RoomKey]:
    return [room for room in rooms if get_room_type(room.business_id) == target_type]
