from pydantic import BaseModel
from typing import List, Dict, Optional

class RoomInput(BaseModel):
    name: str
    url: str
    branch: Optional[str] = None

class AvailableRoomRequest(BaseModel):
    date: str  # YYYY-MM-DD
    hour_slots: List[str]
    rooms: List[RoomInput]

class RoomAvailability(BaseModel):
    name: str
    url: str
    branch: Optional[str]
    available: bool
    available_slots: Dict[str, bool]