import httpx
from groove_checker.config import RESERVE_URL


async def get_reservation_data(client: httpx.AsyncClient,
                               target_date: str,
                               location: str = "sadang") \
        -> str:
    reserve_data = {
        "reserve_date": target_date,
        "gubun": location
    }
    reserve_headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.groove4.co.kr/reservation/reserve.asp"
    }

    try:
        response = await client.post(
            RESERVE_URL,
            data=reserve_data,
            headers=reserve_headers
        )
        return response.text
    except Exception as e:
        print(f"예약 정보 조회 중 오류 발생: {e}")
        return ""


