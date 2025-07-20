class InvalidDateFormatError(ValueError):
    """날짜 형식이 잘못된 경우"""
    pass

class InvalidHourSlotError(ValueError):
    """시간 형식이 잘못된 경우"""
    pass

class InvalidRoomKeyError(ValueError):
    """RoomKey 정보가 유효하지 않을 경우"""
    pass

class ResponseMismatchError(ValueError):
    """요청한 방과 응답한 방의 biz_item_id가 일치하지 않을 때 발생"""
    pass
