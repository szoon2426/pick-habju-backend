# tests/test_groove_service.py
import pytest
from models.dto import AvailabilityResponse, RoomKey
from service.groove_checker import get_groove_availability

@pytest.mark.asyncio
async def test_get_groove_availability():

    # 실제 테스트용 파라미터를 여기에 입력하세요
    date = "2025-07-12"
    hour_slots = ["22:00", "23:00"]
    groove_rooms = [
        RoomKey(name="A룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-A"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-B"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-C")
    ]

    result = await get_groove_availability(date, hour_slots, groove_rooms)
    print(result)  # 가공 없이 그대로 출력

@pytest.mark.asyncio
async def test_time_validation():

    # 잘못된 시간 슬롯이 들어오면 예외가 발생하지 않지만, hour_slots가 비어 있으면 결과가 모두 False여야 함
    result = await get_groove_availability(
        date="2025-07-15",
        hour_slots=[],
        rooms=[
            RoomKey(
                name="A룸",
                branch="그루브 사당점",
                business_id="sadang",
                biz_item_id="groove-A"
            )
        ]
    )
    assert isinstance(result, AvailabilityResponse)
    assert result.results[0].available is True  # 빈 hour_slots면 all([])=True

@pytest.mark.asyncio
async def test_availability_slots(monkeypatch):
    # 실제 HTML 구조에 맞춘 샘플
    sample_html = '''
      <div id="reserve_time_13_17" class="reserve_time_off"></div>
      <div class="on"></div>
      <div id="reserve_time_15_17" class="reserve_time_off"></div>
      <div id="reserve_time_16_17" class="reserve_time_off"></div>
    '''
    # httpx.AsyncClient 모킹
    class DummyClient:
        async def post(self, *args, **kwargs):
            class Resp: text = sample_html
            return Resp()
        async def __aenter__(self): return self
        async def __aexit__(self, *a): pass

    monkeypatch.setattr("services.groove_service.httpx.AsyncClient", lambda: DummyClient())
    svc = GrooveService()
    rooms = [
        RoomKey(
            name="A룸",
            branch="그루브 사당점",
            business_id="sadang",
            biz_item_id="groove-A"
        ),
        RoomKey(
            name="B룸",
            branch="그루브 사당점",
            business_id="sadang",
            biz_item_id="groove-B"
        ),
        RoomKey(
            name="C룸",
            branch="그루브 사당점",
            business_id="sadang",
            biz_item_id="groove-C"
        ),
        RoomKey(
            name="D룸",
            branch="그루브 사당점",
            business_id="sadang",
            biz_item_id="groove-D"
        ),
    ]
    result = await svc.get_groove_availability(
        date="2025-07-15",
        hour_slots=["17:00"],
        rooms=rooms
    )

    # 반환값 타입 체크
    assert isinstance(result, AvailabilityResponse)
    assert len(result.results) == 4

    # 룸별 예약 가능성 체크 (A=13, B=14, C=15, D=16)
    a = next(r for r in result.results if r.biz_item_id == "groove-A")
    b = next(r for r in result.results if r.biz_item_id == "groove-B")
    c = next(r for r in result.results if r.biz_item_id == "groove-C")
    d = next(r for r in result.results if r.biz_item_id == "groove-D")

    assert a.available_slots["17:00"] is True    # 예약 가능
    assert b.available_slots["17:00"] is False   # 예약 불가
    assert c.available_slots["17:00"] is True    # 예약 가능
    assert d.available_slots["17:00"] is True    # 예약 가능

    # 전체 가용성 판단
    assert a.available is True
    assert b.available is False
    assert c.available is True
    assert d.available is True

    # available_biz_item_ids 확인
    assert set(result.available_biz_item_ids) == {"groove-A", "groove-C", "groove-D"}
