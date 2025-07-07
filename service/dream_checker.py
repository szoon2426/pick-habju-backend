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

#date랑 hour_slots의 hour를 드립합주실 response에 맞게 수정해야함
async def get_dream_availability(date, hour_slots, biz_item_id):
    try:
        socket.gethostbyname("xn--hy1bm6g6ujjkgomr.com")
        print("[🔧 DNS 프리패칭 완료]")
    except Exception as e:
        print(f"[⚠️ DNS 프리패칭 실패]: {e}")

    data = {
        'rm_ix': biz_item_id,
        'sch_date': date
    }

    async with httpx.AsyncClient() as client:
      response = await client.post(URL, headers=HEADERS, cookies=COOKIES, data=data)
      response_data = response.json()

    available = {}
    items_html = html.unescape(response_data.get("items", ""))
    for time in hour_slots:
      pattern = fr'<label[^>]*class=["\']([^"\']*btn-time[^"\']*)["\'][^>]*title=["\'][^"\']*{time}[^"\']*["\'][^>]*>'
      match = re.search(pattern, items_html, re.DOTALL)

      if match:
          classes = match.group(1).split()
          available[time] = True if 'active' in classes else False
      else:
          available[time] = False

    return available
