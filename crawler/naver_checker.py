from playwright.async_api import async_playwright
import re

def convert_korean_time(text: str) -> str:
    match = re.match(r'(오전|오후)?\s?(\d{1,2})시', text)
    if not match:
        return None
    period, hour_str = match.groups()
    hour = int(hour_str)
    if period == '오전':
        hour = 0 if hour == 12 else hour
    elif period == '오후':
        hour = 12 if hour == 12 else hour + 12
    return f"{hour:02d}:00"

async def fetch_available_times(url: str, room_name: str, date: str, hour_slots: list[str]) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_timeout(2000)

        result = {}
        try:
            await page.wait_for_selector("li.time_item", timeout=10000)
            time_items = await page.query_selector_all("li.time_item")
        except Exception as e:
            print(f"❌ 시간 슬롯 로딩 실패: {e}")
            await browser.close()
            return {}

        for item in time_items:
            class_attr = await item.get_attribute("class")
            is_available = "disabled" not in class_attr

            time_span = await item.query_selector("span.time_text")
            if not time_span:
                continue

            raw_text = await time_span.inner_text()
            raw_text = raw_text.replace("\n", "").strip()
            converted = convert_korean_time(raw_text)

            if converted in hour_slots:
                result[converted] = is_available

        await browser.close()
        return result