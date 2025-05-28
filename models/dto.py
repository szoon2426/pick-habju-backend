from pydantic import BaseModel
from typing import List, Dict

# 요청 구조 dto
class AvailabilityRequest(BaseModel):
    date: str
    hour_slots: List[str]

# 응답 구조 dto 
class RoomAvailability(BaseModel):
    name: str
    branch: str
    business_id: str
    biz_item_id: str
    available: bool
    available_slots: Dict[str, bool]
