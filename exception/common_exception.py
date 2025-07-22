from exception.base_exception import BaseCustomException

class InvalidDateFormatError(BaseCustomException):
    """날짜 형식이 잘못된 경우"""
    error_code = "Date-001"
    message = "날짜 형식이 잘못되었습니다."
    status_code = 400

class PastDateNotAllowedError(BaseCustomException):
    """과거 날짜는 허용되지 않을 때 발생"""
    error_code = "Date-002"
    message = "과거 날짜는 허용되지 않습니다."
    status_code = 400

class InvalidHourSlotError(BaseCustomException):
    """시간 형식이 잘못된 경우"""
    error_code = "Hour-001"
    message = "시간 형식이 잘못되었습니다."
    status_code = 400

class PastHourSlotNotAllowedError(BaseCustomException):
    """과거 시간은 허용되지 않을 때 발생"""
    error_code = "Hour-002"
    message = "과거 시간은 허용되지 않습니다."
    status_code = 400

class RoomKeyFieldMissingError(BaseCustomException):
    error_code = "Room-001"
    message = "RoomKey 정보가 누락되었습니다."
    status_code = 400

class RoomKeyNotFoundError(BaseCustomException):
    error_code = "Room-002"
    message = "RoomKey가 존재하지 않습니다."
    status_code = 404

class ResponseMismatchError(BaseCustomException):
    """요청한 방과 응답한 방의 biz_item_id가 일치하지 않을 때 발생"""
    error_code = "Response-001"
    message = "요청/응답 biz_item_id 불일치"
    status_code = 500
