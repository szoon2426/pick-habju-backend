class BaseCustomException(Exception):
    error_code: str = "GENERIC-000"
    message: str = "알 수 없는 오류가 발생했습니다."
    status_code: int = 400

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)
