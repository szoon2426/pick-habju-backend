import re
from datetime import datetime
from typing import List
from exception.common.hour_excpetion import InvalidHourSlotError, PastHourSlotNotAllowedError

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
