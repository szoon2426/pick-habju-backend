import httpx
import re
import html
import sys
import socket
import os
import json
import asyncio
from utils.room_loader import load_rooms
from models.dto import RoomKey
from models.dto import RoomAvailability

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

async def get_dream_availability(date, hour_slots, dream_rooms):
   tasks = [dream_room_checker(date, hour_slots, room.biz_item_id) for room in dream_rooms]
   results = await asyncio.gather(*tasks)
   print(results)
   return results


async def dream_room_checker(date, hour_slots, biz_item_id):
    try:
        socket.gethostbyname("xn--hy1bm6g6ujjkgomr.com")
        print("[🔧 DNS 프리패칭 완료]")
    except Exception as e:
        print(f"[⚠️ DNS 프리패칭 실패]: {e}")

    data = {
        'rm_ix': biz_item_id,
        'sch_date': date
    }

    async with httpx.AsyncClient(cookies=COOKIES) as client:
      response = await client.post(URL, headers=HEADERS, data=data)
      response_data = response.json()

    available = True
    available_slots = {}
    items_html = html.unescape(response_data.get("items", ""))

    for time in hour_slots:
      target_time = time.split(":")[0] + "시00분"
      pattern = fr'<label[^>]*class=["\']([^"\']*btn-time[^"\']*)["\'][^>]*title=["\'][^"\']*{target_time}[^"\']*["\'][^>]*>'
      match = re.search(pattern, items_html, re.DOTALL)

      if match:
          classes = match.group(1).split()
          available_slots[time] = True if 'active' in classes else False
      else:
          available_slots[time] = False
      if available_slots[time] == False:
         available = False  
    
    rooms = load_rooms()
    matches = [ (r["name"], r["branch"], r["business_id"]) for r in rooms if r["biz_item_id"] == biz_item_id]
    if matches:
       name, branch, business_id = matches[0]
    
    return RoomAvailability(name = name, branch = branch, business_id=business_id, biz_item_id=biz_item_id, available=available, available_slots=available_slots)
#나만의 테스트 코드
asyncio.run(get_dream_availability("2025-07-08", ["16:00", "17:00"], [RoomKey(name='D룸', branch='드림합주실 사당점', business_id='dream_sadang', biz_item_id='25'), RoomKey(name='C룸', branch='드림합주실 사당점', business_id='dream_sadang', biz_item_id='28')]))