import json

import httpx
import asyncio

from config import RESERVE_URL
from groove_checker.api.auth import login
from groove_checker.utils.parser import parse_reservation_html

async def check_reservation(target_date: str, target_time: str):
    async with httpx.AsyncClient() as client:
        # 로그인 검증
        if not await login(client):
            return []
        # 예약 데이터 요청
        try:
            response = await client.post(
                RESERVE_URL,
                data={"reserve_date": target_date, "gubun": "sadang"},
                headers={"X-Requested-With": "XMLHttpRequest"}
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"예약 데이터 요청 실패: {e}")
            return []
        reservation_html = response.text
        dtos = parse_reservation_html(reservation_html, target_time)
        return [dto.to_dict() for dto in dtos]


# 테스트 코드
async def test():
    # 정상 케이스
    print("=== 정상 테스트 ===")
    result = await check_reservation("2025-05-15", "19:00-20:00")
    print(json.dumps(result, indent=2, ensure_ascii=False))



if __name__ == "__main__":
    asyncio.run(test())


