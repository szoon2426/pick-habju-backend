# te/test_groove_service.py
import pytest
from datetime import datetime, timedelta
from app.models.dto import RoomKey
from app.crawler.groove_checker import get_groove_availability

@pytest.mark.asyncio
async def test_get_groove_availability():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    hour_slots = ["20:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="13"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="14"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="15")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력

@pytest.mark.asyncio
async def test_get_groove_availability1():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-16"
    hour_slots = ["21:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="13"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="14"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="15"),
        RoomKey(name="D룸", branch="그루브 사당점", business_id="sadang", biz_item_id="16")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력
@pytest.mark.asyncio

async def test_get_groove_availability2():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-17"
    hour_slots = ["21:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="13"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="14"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="15")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력
