# crawler/naver_checker.py
from playwright.async_api import async_playwright
import re

def convert_korean_time(text: str) -> str:
    """한글 시간 표현 ('오전 3시', '오후 2시', '5시')를 'HH:MM'으로 변환"""
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

async def fetch_available_times(url: str, room_name: str, date: str, hour_slots: list[str]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        page = await browser.new_page()
        await page.goto(url)
        
        # Step 1: entryIframe 진입
        iframe_element = await page.wait_for_selector('iframe#entryIframe', timeout=10000)
        entry_frame = await iframe_element.content_frame()

        # Step 2: 예약 버튼 클릭
        await entry_frame.wait_for_selector("a[role='button']", timeout=10000)
        buttons = await entry_frame.query_selector_all("a[role='button']")

        for btn in buttons:
            inner_html = await btn.inner_html()
            if "예약" in inner_html:
                await btn.click()
                print("✅ 예약 버튼 클릭 완료")
                break
        else:
            print("❌ 예약 버튼을 찾을 수 없습니다.")
            await browser.close()
            return []
        
        # Step 3: '블랙룸' 텍스트가 포함된 예약 링크 클릭 (iframe 안에서 찾기)
        await entry_frame.wait_for_selector("a.place_bluelink", timeout=10000)
        link_elements = await entry_frame.query_selector_all("a.place_bluelink")

        found = False
        for link in link_elements:
            try:
                title_span = await link.query_selector("span.lsthu")
                if not title_span:
                    continue
                text = await title_span.inner_text()
                if room_name in text:
                    href = await link.get_attribute("href")
                    if not href.startswith("http"):
                        href = "https://m.booking.naver.com" + href
                    await page.goto(href)
                    print(f"✅ '{room_name}' 예약 페이지로 이동 완료: {href}")
                    found = True
                    break
            except Exception as e:
                print("❌ 링크 검사 중 오류:", e)
                continue

        if not found:
            print(f"❌ '{room_name}' 링크를 찾을 수 없습니다.")
            await browser.close()
            return []
        
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(1500)
        
        # Step 4: 날짜 클릭 (page 기준)
        await page.wait_for_selector("button.calendar_date", timeout=10000)
        date_buttons = await page.query_selector_all("button.calendar_date")

        selected_day = date[-2:].lstrip("0")  # 예: "2025-04-05" → "5"
        date_clicked = False
        for btn in date_buttons:
            num_span = await btn.query_selector("span.num")
            if not num_span:
                continue
            text = await num_span.inner_text()
            if text == selected_day:
                is_disabled = await btn.get_attribute("disabled")
                if is_disabled:
                    print(f"❌ {text}일은 선택할 수 없습니다.")
                    break
                await btn.click()
                print(f"✅ {text}일 날짜 클릭 완료")
                date_clicked = True
                break

        if not date_clicked:
            print(f"❌ 날짜 '{selected_day}'을 클릭할 수 없습니다.")
            await browser.close()
            return []
        
        await page.wait_for_timeout(1500)
        print("🔍 시간 슬롯 검사 중...")

        # Step 6: 시간 슬롯 확인
        await page.wait_for_selector("li.time_item.no_time", timeout=10000)
        time_items = await page.query_selector_all("li.time_item")

        result = {}
        for item in time_items:
            class_attr = await item.get_attribute("class")
            is_available = "disabled" not in class_attr

            time_span = await item.query_selector("span.time_text")
            if not time_span:
                print("❌ 시간 텍스트를 찾지 못함")
                continue

            raw_text = await time_span.inner_text()
            raw_text = raw_text.replace("\n", "").strip()
            converted = convert_korean_time(raw_text)

            print(f"🕒 슬롯: '{raw_text}' → {converted} / {'가능' if is_available else '불가능'}")

            if converted and converted in hour_slots:
                result[converted] = is_available

        await browser.close()
        return result