import httpx
from groove_checker.config import LOGIN_ID, LOGIN_PW, LOGIN_URL


async def login(client: httpx.AsyncClient) -> bool:
    login_data = {
        "login_id": LOGIN_ID,
        "login_pw": LOGIN_PW
    }

    login_headers = {
        "Referer": "https://www.groove4.co.kr/member/login.asp",
        "Content-Type": "application/x-www-form-urlencoded"
    }


    try:
        login_res = await client.post(
            LOGIN_URL,
            data=login_data,
            headers=login_headers
        )
        return login_res.status_code == 200
    except httpx.HTTPStatusError as e:
        print(f"HTTP 오류 발생: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return False
