import pytest
from datetime import datetime, timedelta
from models.dto import RoomKey
from models.dto import RoomAvailability
from service.dream_checker import get_dream_availability

@pytest.mark.asyncio
async def test_get_dream_availability():
  date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
  rooms = [
        RoomKey(name="D룸", branch="드림합주실 사당점", business_id="dream_sadang", biz_item_id="29"),
        RoomKey(name="C룸", branch="드림합주실 사당점", business_id="dream_sadang", biz_item_id="28"),
    ]
  result = await get_dream_availability(date, ["13:00", "14:00"], rooms)
  # ✅ 결과가 리스트인지 확인
  assert isinstance(result, list)
  assert len(result) == 2

  # ✅ 각 요소에 필요한 키가 들어있는지 확인
  for room_result in result:
      assert isinstance(room_result, RoomAvailability)
