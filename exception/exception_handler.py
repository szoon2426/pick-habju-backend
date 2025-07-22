from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
from exception.common_exception import BaseCustomException

async def custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": exc.status_code,
            "errorCode": exc.error_code,
            "message": exc.message
        }
    )
