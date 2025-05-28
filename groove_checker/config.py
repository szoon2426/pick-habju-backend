import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LOGIN_ID = os.getenv("LOGIN_ID")
LOGIN_PW = os.getenv("LOGIN_PW")

BASE_URL = os.getenv("BASE_URL", "https://www.groove4.co.kr")
LOGIN_URL = f"{BASE_URL}/member/login_exec.asp"
RESERVE_URL = f"{BASE_URL}/reservation/reserve_table_view.asp"

def load_room_map():
    config_path = Path(__file__).parent / "rooms.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("rooms", {})
    except Exception as e:
        print(f"룸 정보 로드 실패: {e}")
        return {}

ROOM_MAP = load_room_map()


