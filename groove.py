from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver():
    # 크롬 옵션 설정
    chrome_options = Options()

    # 이미지 로딩 비활성화 (빠른 로딩을 위해)
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    # 기타 성능 향상 옵션들
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')

    # 브라우저 시작
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def login_to_groove4(driver, username, password):
    # 로그인 페이지 접속
    driver.get('https://www.groove4.co.kr/member/login.asp')

    # 명시적 대기 설정 (최대 10초까지 기다림)
    wait = WebDriverWait(driver, 10)

    # 아이디와 비밀번호 입력 필드가 나타날 때까지 기다림
    login_id = wait.until(EC.presence_of_element_located((By.ID, 'login_id')))
    login_id.send_keys(username)

    login_pw = driver.find_element(By.ID, 'login_pw')
    login_pw.send_keys(password)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, '//input[@type="image"][@alt="로그인"]')
    login_button.click()

    # 로그인 완료될 때까지 대기
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Reservation 사당")]')))


def get_reservation_info(driver, date, current_page_date=None):
    # 이미 해당 날짜 페이지에 있는지 확인
    if date == current_page_date:
        # 이미 같은 날짜를 보고 있으므로 페이지 이동 없이 그대로 사용
        pass
    else:
        # 다른 날짜로 이동해야 함
        try:
            # 예약 페이지에 처음 접근하는 경우
            if current_page_date is None:
                # 사당점 예약 페이지로 이동
                reservation_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Reservation 사당")]'))
                )
                reservation_link.click()

            # 날짜 선택
            date_script = f"setReserveDate('{date}');"
            driver.execute_script(date_script)

        except Exception as e:
            print(f"페이지 이동 중 오류: {e}")
            # 오류 발생 시 예약 페이지로 다시 접근
            reservation_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Reservation 사당")]'))
            )
            reservation_link.click()

            # 날짜 선택 재시도
            date_script = f"setReserveDate('{date}');"
            driver.execute_script(date_script)

    # 페이지 로딩 대기 (테이블이 로드될 때까지)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="reserve_time_"]'))
    )

    # 자바스크립트로 예약 정보 추출
    script = """
    var result = [];
    var elements = document.querySelectorAll('[id^="reserve_time_"][class*="reserve_time_off"]');

    elements.forEach(function(el) {
        var id = el.id;
        var onclick = el.getAttribute('onclick');

        if (onclick && onclick.includes('setReserveTime')) {
            var parts = id.split('_');
            var roomId = parts[2];
            var timeId = parts[3];

            // onclick에서 가격 추출 (이미지에서 본 형식 기반)
            var priceMatch = onclick.match(/setReserveTime\\(\\d+,\\s*'[^']*',\\s*\\d+,\\s*(\\d+)/);
            var price = priceMatch ? priceMatch[1] : 'N/A';

            result.push({
                room_id: roomId,
                time: timeId,
                price: price,
                raw_onclick: onclick
            });
        }
    });

    return result;
    """

    # JavaScript로 데이터 추출
    raw_data = driver.execute_script(script)

    # 결과 가공
    reservation_info = []

    # 룸 이름 매핑
    rooms = {
        '13': 'A룸',
        '14': 'B룸',
        '15': 'C룸',
        '16': 'D룸'
    }

    # 시간 매핑
    time_map = {str(i): f"{i}:00-{i + 1}:00" for i in range(9, 24)}
    # 24시 이후 시간 추가
    time_map.update({
        '24': '00:00-01:00',
        '25': '01:00-02:00',
        '26': '02:00-03:00',
        '27': '03:00-04:00',
        '28': '04:00-05:00',
        '29': '05:00-06:00'
    })

    for item in raw_data:
        room_id = item['room_id']
        # 알려진 룸 ID인 경우에만 정보 추가 (13, 14, 15, 16)
        if room_id in rooms:
            room_name = rooms[room_id]
            time_id = item['time']
            time_str = time_map.get(time_id, f"{time_id}:00-{int(time_id) + 1}:00")

            info = {
                'room_id': room_id,
                'room_name': room_name,
                'time': time_str,
                'price': item['price'],
                'date': date
            }

            reservation_info.append(info)

    # 현재 보고 있는 페이지의 날짜를 반환
    return reservation_info, date

def main():
    # 로그인 정보
    username = 'kksu149'
    password = 'rudtn0409!'

    # 날짜 목록
    dates = [
        '2025-05-05', '2025-05-06', '2025-05-07', '2025-05-08', '2025-05-09',
        '2025-05-10', '2025-05-11', '2025-05-12', '2025-05-13'
    ]

    # 드라이버 설정
    driver = setup_driver()

    try:
        # 로그인
        login_to_groove4(driver, username, password)

        # 날짜별로 순차적으로 처리
        current_page_date = None  # 현재 보고 있는 페이지의 날짜

        for date in dates:
            try:
                # 예약 정보 가져오기
                reservation_info, current_page_date = get_reservation_info(driver, date, current_page_date)

                # 결과 출력 - 예약 정보가 있는 경우에만 출력
                if reservation_info:
                    print(f"\n===== {date} 예약 정보 =====")
                    for info in reservation_info:
                        print(f"{info['room_name']} ({info['time']}): {info.get('price', 'N/A')}원")
                # 예약 정보가 없으면 아무것도 출력하지 않음

            except Exception as e:
                # 오류가 발생해도 출력하지 않음
                # 오류 디버깅이 필요하면 아래 주석을 해제하세요
                # print(f"{date} 처리 중 오류 발생: {e}")

                # 오류가 발생하면 현재 페이지 상태를 초기화
                current_page_date = None

    finally:
        # 브라우저 닫기
        driver.quit()


if __name__ == "__main__":
    main()
