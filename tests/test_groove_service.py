# tests/test_groove_service.py
import pytest
from models.dto import AvailabilityResponse, RoomKey
from service.groove_checker import get_groove_availability

@pytest.mark.asyncio
async def test_get_groove_availability():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-15"
    hour_slots = ["21:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-A"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-B"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-C")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력

@pytest.mark.asyncio
async def test_get_groove_availability1():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-16"
    hour_slots = ["21:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-A"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-B"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-C"),
        RoomKey(name="D룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-D")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력
@pytest.mark.asyncio

async def test_get_groove_availability2():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-17"
    hour_slots = ["21:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-A"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-B"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-C")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력
