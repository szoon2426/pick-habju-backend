from fastapi import FastAPI
from api.available_room import router as available_router

app = FastAPI()
app.include_router(available_router)