import httpx
import asyncio
import re
import html
import sys
import time
import socket

sys.stdout.reconfigure(encoding='utf-8')

URL = "https://www.xn--hy1bm6g6ujjkgomr.com/plugin/wz.bookingT1.prm/ajax.calendar.time.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}
COOKIES = {
    'PHPSESSID': 'bnm9bi650n935hea9bipq2dcl7',
    'e1192aefb64683cc97abb83c71057733': 'Ym9va2luZw%3D%3D'
}

def get_date():
    date = input("예약하실 날짜를 입력해주세요!(ex 2025-05-30)\n")    
    return date

def get_timeList():
    time = input("예약하실 시간을 입력해주세요!(ex 11, 12)\n")
    timeList = [x.strip() for x in time.split(",")]
    return timeList

async def is_time_available(client: httpx.AsyncClient, rm_ix: str, sch_date: str, target_time: str):
    print(f"\n[⏱️ 시작] 방 {rm_ix} - {sch_date} - {target_time}")
    start_time = time.time()

    data = {
        'rm_ix': rm_ix,
        'sch_date': sch_date
    }

    try:
        response = await client.post(URL, headers=HEADERS, cookies=COOKIES, data=data)

        if response.status_code == 200:
            response_data = response.json()
            items_html = html.unescape(response_data.get("items", ""))

            pattern = fr'<label[^>]*class=["\']([^"\']*btn-time[^"\']*)["\'][^>]*title=["\'][^"\']*{target_time}[^"\']*["\'][^>]*>'
            match = re.search(pattern, items_html, re.DOTALL)

            if match:
                classes = match.group(1).split()
                result = '가능' if 'active' in classes else '불가능'
            else:
                result = '불가능'
        else:
            result = '불가능'
    except Exception as e:
        print(f"[⚠️ Error] 방 {rm_ix} 요청 중 오류 발생: {e}")
        result = '불가능'

    done_time = time.time()
    duration = done_time - start_time
    print(f"[⏱️ 완료] 방 {rm_ix} - {target_time} 소요 시간: {duration:.4f}초")
    return (target_time, result, done_time, duration)

async def check_room_times(client: httpx.AsyncClient, rm_ix: str, sch_date: str, times: list[str]):
    tasks = [is_time_available(client, rm_ix, sch_date, t) for t in times]
    results = await asyncio.gather(*tasks)

    is_all_available = all(result[1] == "가능" for result in results)
    done_time = max(r[2] for r in results)
    total_duration = sum(r[3] for r in results)

    return (rm_ix, "가능" if is_all_available else "불가능", done_time, total_duration)

async def main():
    prestart = time.time()
    print(f"[🚀 main() 진입 시각]: {prestart:.4f}")

    try:
        socket.gethostbyname("xn--hy1bm6g6ujjkgomr.com")
        print("[🔧 DNS 프리패칭 완료]")
    except Exception as e:
        print(f"[⚠️ DNS 프리패칭 실패]: {e}")

    sch_date = get_date()
    times_to_check = get_timeList()  # ✅ main에서 시간 지정
    room_ids = ["25", "26", "27", "28", "29"]

    async with httpx.AsyncClient() as client:
        client_ready = time.time()
        print(f"[📡 client 준비 완료 시각]: {client_ready:.4f} | 준비 소요: {client_ready - prestart:.4f}초")

        main_start = time.time()
        print(f"[🔄 task 실행 직전 시각]: {main_start:.4f}")

        tasks = [check_room_times(client, rm_ix, sch_date, times_to_check) for rm_ix in room_ids]
        results = await asyncio.gather(*tasks)

    received_time = time.time()

    print("\n[🔎 전체 결과]")
    for rm_ix, result, done_time, duration in results:
        print(f"방 {rm_ix}: {result} | "
              f"처리 소요 시간: {duration:.4f}초 | "
              f"main 수령까지 지연: {received_time - done_time:.4f}초 | "
              f"main 시작 이후 총 소요: {received_time - main_start:.4f}초")

    total_end = time.time()
    print(f"\n[✅ 전체 작업 완료] 총 소요 시간: {total_end - prestart:.4f}초")

# 실행
asyncio.run(main())
