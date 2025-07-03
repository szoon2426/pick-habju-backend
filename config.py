import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROOVE_LOGIN_ID = os.getenv("GROOVE_LOGIN_ID")
GROOVE_LOGIN_PW = os.getenv("GROOVE_LOGIN_PW")
GROOVE_BASE_URL = os.getenv("GROOVE_BASE_URL")
DREAM_LOGIN_ID = os.getenv("DREAM_LOGIN_ID")
DREAM_LOGIN_PW = os.getenv("DREAM_LOGIN_PW")
DREAM_BASE_URL = os.getenv("DREAM_BASE_URL")

GROOVE_LOGIN_URL = f"{GROOVE_BASE_URL}/member/login_exec.asp"
GROOVE_RESERVE_URL = f"{GROOVE_BASE_URL}/reservation/reserve_table_view.asp"
