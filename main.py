import asyncio
from crawler.naver_checker import fetch_available_times

if __name__ == "__main__":
    result = asyncio.run(fetch_available_times(
        url="https://map.naver.com/p/entry/place/1712597581?c=14.98,0,0,0,dh",
        room_name="블랙룸",
        date="2025-06-10",
        hour_slots=["11:00"]
    ))
    
    print("예약 가능 여부:")
    if isinstance(result, dict):
        for time, available in result.items():
            print(f"{time}: {'가능' if available else '불가능'}")
    else:
        print("❌ 예약 가능한 시간이 없습니다.")
