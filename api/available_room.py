from fastapi import APIRouter
from models import AvailableRoomRequest, RoomAvailability
from crawler.naver_checker import fetch_available_times

router = APIRouter()

@router.post("/available-room", response_model=list[RoomAvailability])
async def check_available_rooms(data: AvailableRoomRequest):
    results = []

    for room in data.rooms:
        try:
            result = await fetch_available_times(
                url=room.url,
                room_name=room.name,
                date=data.date,
                hour_slots=data.hour_slots
            )
            
            is_all_available = all(result.get(slot, False) for slot in data.hour_slots)
            
            results.append(RoomAvailability(
                name=room.name,
                url=room.url,
                branch=room.branch,
                available=is_all_available,
                available_slots=result
            ))
        except Exception as e:
            print(f"❌ {room.name} 확인 중 오류: {e}")
            results.append(RoomAvailability(
                name=room.name,
                url=room.url,
                branch=room.branch,
                available=False,
                available_slots={}
            ))

    return results