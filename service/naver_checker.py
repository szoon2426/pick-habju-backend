import httpx
from typing import List, Dict, Union
from models.dto import RoomKey, RoomAvailability
from exception.naver_exception import NaverAvailabilityError
from utils.validate.common_validator import (
    validate_date, validate_hour_slots, validate_room_key,  InvalidDateFormatError,
    InvalidHourSlotError,
    InvalidRoomKeyError,
)
import asyncio


RoomResult = Union[RoomAvailability, Exception]

async def fetch_naver_availability_room(date: str, hour_slots: List[str], room: RoomKey) -> RoomAvailability:
    url = "https://booking.naver.com/graphql?opName=schedule"
    start_dt = f"{date}T00:00:00"
    end_dt = f"{date}T23:59:59"
    headers = {"Content-Type": "application/json"}
    body = {
        "operationName": "schedule",
        "query": """
        query schedule($scheduleParams: ScheduleParams) {
          schedule(input: $scheduleParams) {
            bizItemSchedule {
              hourly {
                unitStartTime
                unitStock
                unitBookingCount
              }
            }
          }
        }""",
        "variables": {
            "scheduleParams": {
                "businessTypeId": 10,
                "businessId": room.business_id,
                "bizItemId": room.biz_item_id,
                "startDateTime": start_dt,
                "endDateTime": end_dt,
                "fixedTime": True,
                "includesHolidaySchedules": True
            }
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            raise NaverAvailabilityError(f"[{room.name}] 네이버 API 호출 오류: {e}")

    try:
        available_slots: Dict[str, bool] = {}
        for slot in data["data"]["schedule"]["bizItemSchedule"]["hourly"]:
            time_str = slot["unitStartTime"][-8:]
            hour_min = time_str[:5]
            if hour_min in hour_slots:
                available_slots[hour_min] = slot["unitBookingCount"] < slot["unitStock"]
    except Exception as e:
        raise NaverAvailabilityError(f"[{room.name}] 응답 파싱 오류: {e}")

    available = all(available_slots.values())
    return RoomAvailability(
        name=room.name,
        branch=room.branch,
        business_id=room.business_id,
        biz_item_id=room.biz_item_id,
        available=available,
        available_slots=available_slots
    )


async def get_naver_availability(
    date: str,
    hour_slots: List[str],
    naver_rooms: List[RoomKey]
) -> List[RoomResult]:
    try:
        validate_date(date)
    except InvalidDateFormatError as e:
        print(f"[날짜 형식 오류]: {e}")
        raise

    try:
        validate_hour_slots(hour_slots,date)
    except InvalidHourSlotError as e:
        print(f"[시간 형식 오류]: {e}")
        raise

    async def safe_fetch(room: RoomKey) -> RoomResult:
        try:
            validate_room_key(room)
            return await fetch_naver_availability_room(date, hour_slots, room)
        except (InvalidRoomKeyError, NaverAvailabilityError) as e:
            return e

    return await asyncio.gather(*[safe_fetch(room) for room in naver_rooms])
