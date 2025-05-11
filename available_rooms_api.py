import httpx
import asyncio
import re
import html
import sys

# UTF-8로 강제 설정
sys.stdout.reconfigure(encoding='utf-8')

async def is_time_available(rm_ix: str, sch_date: str, target_time: str):
    """
    특정 날짜와 시간대가 예약 가능한지 확인하는 함수
    """
    url = "https://www.xn--hy1bm6g6ujjkgomr.com/plugin/wz.bookingT1.prm/ajax.calendar.time.php"
    cookies = {
        'PHPSESSID': 'bnm9bi650n935hea9bipq2dcl7',
        'e1192aefb64683cc97abb83c71057733': 'Ym9va2luZw%3D%3D'
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'rm_ix': rm_ix,
        'sch_date': sch_date
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, cookies=cookies, data=data)
        #return <- response 자체만으로도 1.946초걸림
        if response.status_code == 200:
            # 🔎 JSON 파싱
            response_data = response.json()
            items_html = response_data.get("items", "")

            # 🔍 HTML Unescape (이스케이프 문자 해제)
            items_html = html.unescape(items_html)

#            print("🔍 [DEBUG] Unescaped HTML:")
#            print(items_html[:500])  # 상위 500자 출력
            #return
            # 🔎 정규 표현식으로 <label>과 <input> 탐색 (줄바꿈도 허용)
            pattern = fr'<label[^>]*class=["\']([^"\']*btn-time[^"\']*)["\'][^>]*>.*?<input[^>]*data-time=["\']{target_time}["\'][^>]*>'
            match = re.search(pattern, items_html, re.DOTALL)

            if match:
                #print(f"🔍 [DEBUG] Match Found: {match.group(0)}")
                # 클래스 목록을 가져와서 active가 있는지 확인
                classes = match.group(1).split()
                if 'btn-time' in classes and 'active' in classes:
                    print(f"[✅ Available] {sch_date} - {target_time} 예약 가능")
                    return True
                else:
                    print(f"[❌ Not Available] {sch_date} - {target_time} 예약 불가능")
                    return False
            else:
                print(f"[❌ Not Found] {sch_date} - {target_time} 시간대를 찾지 못함")
                print("Items HTML (500자 미리보기):\n", items_html[:500])  # 디버깅용
                return False
        else:
            print(f"[❌ Failed] Could not fetch data for {sch_date} - Status Code: {response.status_code}")
            return False


async def main():
    # 파라미터 설정
    rm_ix = "25"
    sch_date = "2025-05-13"
    target_time = "03:00"

    # 예약 가능 여부 확인
    is_available = await is_time_available(rm_ix, sch_date, target_time)
    print(f"{target_time} 예약 가능 여부: {'가능' if is_available else '불가능'}")

# 실행
asyncio.run(main())
