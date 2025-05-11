import httpx
from bs4 import BeautifulSoup
import asyncio


async def check_reservation(target_date: str, target_time: str):
    async with httpx.AsyncClient() as client:
        login_url = "https://www.groove4.co.kr/member/login_exec.asp"
        login_data = {
            "login_id": "kksu149",
            "login_pw": "rudtn0409!"
        }
        login_headers = {
            "Referer": "https://www.groove4.co.kr/member/login.asp",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        login_res = await client.post(
            login_url,
            data=login_data,
            headers=login_headers
        )

        reserve_url = "https://www.groove4.co.kr/reservation/reserve_table_view.asp"
        reserve_data = {
            "reserve_date": target_date,
            "gubun": "sadang"
        }
        reserve_headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.groove4.co.kr/reservation/reserve.asp"
        }

        response = await client.post(
            reserve_url,
            data=reserve_data,
            headers=reserve_headers
        )

        soup = BeautifulSoup(response.text, "html.parser")
        room_map = {
            "13": {"name": "A룸", "price": 22000},
            "14": {"name": "B룸", "price": 20000},
            "15": {"name": "C룸", "price": 17000},
            "16": {"name": "D룸", "price": 15000}
        }

        results = []
        for element in soup.select('[id^="reserve_time_"][class*="off"]'):
            element_id = element.get("id", "")
            parts = element_id.split("_")

            if len(parts) != 4:
                continue

            room_id = parts[2]
            time_id = parts[3]

            if room_id not in room_map:
                continue

            start_hour = int(time_id)
            end_hour = (start_hour + 1) % 24
            time_range = f"{start_hour:02}:00-{end_hour:02}:00"

            if time_range == target_time:
                results.append({
                    "room": room_map[room_id]["name"],
                    "time": time_range,
                    "price": room_map[room_id]["price"]
                })

        return results

# 테스트 코드
async def test():
    result = await check_reservation("2025-05-15", "17:00-18:00")
    print("테스트 결과:", result)

if __name__ == "__main__":
    asyncio.run(test())

