# tests/test_room_router.py

from utils.room_router import filter_rooms_by_type
from models.dto import RoomKey

def test_filter_rooms_by_type_print():
    rooms = [
        RoomKey(name="D룸", branch="드림합주실 사당점", business_id="dream_sadang", biz_item_id="29"),
        RoomKey(name="C룸", branch="드림합주실 사당점", business_id="dream_sadang", biz_item_id="28"),
        RoomKey(name="B룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-B"),
        RoomKey(name="C룸", branch="그루브 사당점", business_id="sadang", biz_item_id="groove-C"),
        RoomKey(name="Classic", branch="비쥬합주실 3호점", business_id="917236", biz_item_id="5098039"),
        RoomKey(name="R룸", branch="준사운드 사당점", business_id="1384809", biz_item_id="6649826"),
    ]
    dream_rooms = filter_rooms_by_type(rooms, "dream")
    groove_rooms = filter_rooms_by_type(rooms, "groove")
    naver_rooms = filter_rooms_by_type(rooms, "naver")

    print("dream_rooms:", [r.biz_item_id for r in dream_rooms])
    print("groove_rooms:", [r.biz_item_id for r in groove_rooms])
    print("naver_rooms:", [r.biz_item_id for r in naver_rooms])

    # 아래는 실제 테스트 검증용 (필요시)
    assert all(r.branch == "드림합주실 사당점" for r in dream_rooms)
    assert all("그루브" in r.branch for r in groove_rooms)
    assert all("드림합주실" not in r.branch and "그루브" not in r.branch for r in naver_rooms)
