from bs4 import BeautifulSoup
from typing import List, Dict
from groove_checker.config import ROOM_MAP
from groove_checker.models.room import Room, Reservation, RoomAvailabilityDTO

def parse_available_slots(soup: BeautifulSoup, target_range: str) -> Dict[str, Dict[str, bool]]:
    """모든 방의 예약 가능 시간대 추출 (타겟 시간 범위만)"""
    room_slots = {rid: {} for rid in ROOM_MAP}

    # 타겟 시간 범위 파싱
    start_str, end_str = target_range.split("-")
    start_h = int(start_str.split(":")[0])
    end_h = int(end_str.split(":")[0])
    target_hours = range(start_h, end_h)

    for element in soup.select('[id^="reserve_time_"]'):
        element_id = element.get("id", "")
        element_class = element.get("class", [])

        parts = element_id.split("_")
        if len(parts) != 4:
            continue

        room_id, time_id = parts[2], parts[3]
        if room_id not in ROOM_MAP:
            continue

        start_hour = int(time_id)
        time_slot = f"{start_hour:02}:00-{(start_hour + 1):02}:00"

        # 타겟 시간대에 포함되는지 확인
        if start_hour not in target_hours:
            continue

        is_available = "off" not in element_class  # 혹은 "on" not in element_class
        room_slots[room_id][time_slot] = is_available

    return room_slots



def validate_time_range(target_range: str) -> tuple[int, int]:
    """시간 범위 유효성 검증"""
    try:
        start_str, end_str = target_range.split("-")
        start_h = int(start_str.split(":")[0])
        end_h = int(end_str.split(":")[0])
        if start_h >= end_h:
            raise ValueError("잘못된 시간 범위")
        return start_h, end_h
    except Exception as e:
        raise ValueError(f"시간 파싱 오류: {e}")


def create_dtos(
        room_slots: Dict[str, Dict[str, bool]],
        target_range: str
) -> List[RoomAvailabilityDTO]:
    """DTO 객체 생성"""
    start_h, end_h = validate_time_range(target_range)
    target_hours = range(start_h, end_h)
    results = []

    for room_id, slots in room_slots.items():
        try:
            room = Room.from_id(room_id)

            target_slots = {}
            all_available = True

            for h in target_hours:
                time_slot = f"{h:02}:00-{(h + 1):02}:00"
                is_available = slots.get(time_slot, False)
                target_slots[time_slot] = is_available

                if not is_available:
                    all_available = False

            if all_available:
                dto = RoomAvailabilityDTO.from_reservation(
                    Reservation(room=room, time=target_range),
                    available_slots=target_slots
                )
                results.append(dto)

        except ValueError as e:
            print(f"룸 처리 오류: {e}")
            continue

    return results


def parse_reservation_html(html: str, target_range: str) -> List[RoomAvailabilityDTO]:
    soup = BeautifulSoup(html, "html.parser")
    room_slots = parse_available_slots(soup, target_range)  # 타겟 시간 전달
    return create_dtos(room_slots, target_range)
