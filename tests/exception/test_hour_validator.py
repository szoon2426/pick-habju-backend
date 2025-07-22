import pytest
from utils.validate.common.hour_validator import validate_hour_slot_format, validate_hour_slot_not_past
from exception.common.hour_excpetion import InvalidHourSlotError, PastHourSlotNotAllowedError
from datetime import datetime, timedelta

# 형식 실패 케이스
def test_validate_hour_slots_invalid_format():
    """'9:00' 형식은 잘못된 시간 형식이며 InvalidHourSlotError 예외가 발생해야 한다 (정규식 미통과)."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(InvalidHourSlotError):
        validate_hour_slot_format(["9:00"], tomorrow)  # 잘못된 형식

# 과거시간대 검증 성공 케이스
def test_validate_hour_slots_valid_today():
    """오늘 날짜 기준으로 현재 시각 이후의 시간대는 유효한 슬롯으로 통과되어야 한다."""
    now = datetime.now()
    # 현재 시간보다 1시간 뒤
    slot = (now + timedelta(hours=1)).strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")
    validate_hour_slot_not_past([slot], today)

def test_validate_hour_slots_future_date():
    """미래 날짜라면 시간 값이 과거든 현재든 관계없이 모두 유효한 슬롯으로 인정된다."""
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    validate_hour_slot_not_past(["00:00", "23:59"], future_date)

# 과거시간대 검증 실패 케이스
def test_validate_hour_slots_past_time_today():
    """오늘 날짜인데 과거 시간대를 포함하면 PastHourSlotNotAllowedError 예외가 발생해야 한다."""
    now = datetime.now()
    # 현재 시간보다 1시간 전
    slot = (now - timedelta(hours=1)).strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")
    with pytest.raises(PastHourSlotNotAllowedError):
        validate_hour_slot_not_past([slot], today)
