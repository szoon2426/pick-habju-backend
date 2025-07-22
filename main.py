from fastapi import FastAPI
from api.available_room import router as available_router
from exception import custom_exception_handler
from exception.common_exception import BaseCustomException

app = FastAPI()
app.include_router(available_router)

app.add_exception_handler(BaseCustomException, custom_exception_handler)
