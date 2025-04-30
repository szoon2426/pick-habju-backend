from fastapi import APIRouter
from models import AvailabilityRequest, RoomAvailability
from crawler.naver_checker import check_availability
import asyncio
from room import rooms

router = APIRouter()

@router.post("/available-rooms", response_model=list[RoomAvailability])
async def available_room(data: AvailabilityRequest):
    async def fetch(room):
        try:
            result = await check_availability(
                business_id=room["business_id"],
                biz_item_id=room["biz_item_id"],
                date=data.date,
                hour_slots=data.hour_slots
            )
            available = all(result.get(slot, False) for slot in data.hour_slots)
            return RoomAvailability(
                name=room["name"],
                branch=room["branch"],
                business_id=room["business_id"],
                biz_item_id=room["biz_item_id"],
                available=available,
                available_slots=result
            )
        except Exception as e:
            print(f"❌ {room['name']} 확인 중 오류:", e)
            return RoomAvailability(
                name=room["name"],
                branch=room["branch"],
                business_id=room["business_id"],
                biz_item_id=room["biz_item_id"],
                available=False,
                available_slots={}
            )

    results = await asyncio.gather(*[fetch(room) for room in rooms])
    return results