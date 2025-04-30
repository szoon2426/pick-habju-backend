from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from crawler.naver_checker import check_availability
from room import rooms

router = APIRouter()

class AvailableRoomRequest(BaseModel):
    date: str
    hour_slots: List[str]

class RoomAvailability(BaseModel):
    name: str
    branch: str
    business_id: str
    biz_item_id: str
    available: bool
    available_slots: Dict[str, bool]

@router.post("/available-rooms", response_model=List[RoomAvailability])
async def available_rooms(request: AvailableRoomRequest):
    results = []
    for room in rooms:
        try:
            slots = check_availability(room["business_id"], room["biz_item_id"], request.date, request.hour_slots)
            is_available = all(slots.get(slot, False) for slot in request.hour_slots)

            results.append(RoomAvailability(
                name=room["name"],
                branch=room["branch"],
                business_id=room["business_id"],
                biz_item_id=room["biz_item_id"],
                available=is_available,
                available_slots=slots
            ))
        except Exception as e:
            results.append(RoomAvailability(
                name=room["name"],
                branch=room["branch"],
                business_id=room["business_id"],
                biz_item_id=room["biz_item_id"],
                available=False,
                available_slots={}
            ))
    return results