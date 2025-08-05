from fastapi import FastAPI
from app.api.available_room import router as available_router
from app.exception.base_exception import BaseCustomException
from app.exception.exception_handler import custom_exception_handler

app = FastAPI()
app.include_router(available_router)

app.add_exception_handler(BaseCustomException, custom_exception_handler)
