import re
from datetime import datetime, timedelta
from typing import List
from app.exception.common.hour_excpetion import InvalidHourSlotError, PastHourSlotNotAllowedError

HOUR_PATTERN = r"^\d{2}:\d{2}$"

def validate_hour_slot_format(slot: str):
    """시간 형식(HH:MM) 검증"""
    if not re.match(HOUR_PATTERN, slot):
        raise InvalidHourSlotError(f"시간 형식이 잘못되었습니다: {slot}")

def validate_hour_slot_not_past(slot: str, now_time):
    """슬롯이 과거 시간인지 검증"""
    slot_time = datetime.strptime(slot, "%H:%M").time()
    if slot_time < now_time:
        raise PastHourSlotNotAllowedError(f"과거 시간은 허용되지 않습니다: {slot}")

def validate_hour_slots(hour_slots: List[str], date: str):
    """시간 슬롯 전체 검증(형식 + 과거여부)"""
    now = datetime.now()
    today = now.date()
    input_date = datetime.strptime(date, "%Y-%m-%d").date()
    for slot in hour_slots:
        validate_hour_slot_format(slot)
        if input_date == today:
            validate_hour_slot_not_past(slot, now.time())

def validate_hour_continuous(hour_slots: List[str], date: str):
    """입력받은 시간값이 연속한지 검증"""
    # 시간 문자열을 datetime 객체 리스트로 변환
    time_format = "%H:%M"
    times = [datetime.strptime(slot, time_format).time() for slot in hour_slots]

    # 시간 순서대로 정렬
    times.sort()

    # 인접한 시간 간격이 1시간(1시간 간격의 연속)인지 확인
    for i in range(len(times) - 1):
        dt_current = datetime.combine(datetime.today(), times[i])
        dt_next = datetime.combine(datetime.today(), times[i+1])
        diff = dt_next - dt_current
        if diff != timedelta(hours=1):
            raise ValueError(f"시간 슬롯이 연속적이지 않습니다: {hour_slots[i]}와 {hour_slots[i+1]} 사이에 간격이 1시간이 아닙니다.")

    # 날짜가 오늘이면 과거 시간인지 체크하는 기존 로직
    now = datetime.now()
    today = now.date()
    input_date = datetime.strptime(date, "%Y-%m-%d").date()
    if input_date == today:
        for slot in hour_slots:
            validate_hour_slot_not_past(slot, now.time())
