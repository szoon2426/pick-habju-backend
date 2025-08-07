from app.exception.base_exception import BaseCustomException

class RequestFailedError(BaseCustomException):
    """날짜 형식이 잘못된 경우"""
    error_code = "API-001"
    message = "API 응답 요청 실패 오류:"
    status_code = 422