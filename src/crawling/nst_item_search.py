
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import pandas as pd


def select_dropdown_option(driver, button_id: str, option_xpath: str):
    """
    드롭다운 버튼을 클릭한 후 지정된 옵션을 선택
    
    Args:
        driver: Selenium WebDriver 객체
        button_id (str): 드롭다운 버튼의 ID
        option_xpath (str): 선택할 옵션의 XPath
    """
    # element = driver.find_element(By.XPATH, option_xpath)
    # print(option_xpath)
    # print("Displayed:", element.is_displayed())  # 요소가 화면에 표시되는지 확인
    # print("Enabled:", element.is_enabled())      # 요소가 활성화 상태인지 확인
    try:
        # 드롭다운 버튼 클릭
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, button_id))
        )
        dropdown_button.click()

        # 드롭다운 항목 선택
        dropdown_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        dropdown_option.click()

    except Exception as e:
        print(f"오류 발생: {e}")
        driver.save_screenshot("debug_screenshot.png")


def toggle_checkbox(driver, checkbox_id: str, check: bool=True):
    """
    체크박스를 선택하거나 선택 해제

    Args:
        driver: Selenium WebDriver 객체
        checkbox_id (str): 체크박스의 ID (예: "item_age_1")
        check (bool): True일 경우 체크, False일 경우 체크 해제
    """
    # 체크박스 요소 가져오기
    checkbox = driver.find_element(By.ID, checkbox_id)

    # 현재 체크 상태 확인
    is_checked = checkbox.is_selected()

    # 체크 상태 변경
    if check and not is_checked:
        checkbox.click()
    elif not check and is_checked:
        checkbox.click()

    # print(f"체크박스 {checkbox_id} {'선택' if check else '해제'} 완료")


def input_keyword(driver, baseline_keyword: str, input_keyword: str):
    """
    주제어와 추가 키워드를 입력

    Args:
        driver: Selenium WebDriver 객체
        keyword: 입력할 키워드
    """
    # if len(additional_keywords) > 4:
    #     raise ValueError(f"키워드 수({len(additional_keywords)})가 입력 가능한 필드 수를 초과했습니다.")
    # 키워드 입력
    # baseline_keyword = "게임"  # 비교 기준이 되는 키워드
    
    # 운영 체제에 따라 CONTROL 또는 COMMAND 키 선택
    # print(platform.system())
    if platform.system() == "Darwin":  # macOS
        modifier_key = Keys.COMMAND
        # print("run in mac")
    else:  # Windows/Linux
        modifier_key = Keys.CONTROL


    for i, keyword in enumerate([baseline_keyword] + [input_keyword]):
        query = keyword  # + " 게임" if i > 0 else keyword
        field_id = f"item_keyword{i+1}"
        input_box = driver.find_element(By.ID, field_id)
        input_box.send_keys(modifier_key + "A")
        time.sleep(.1)
        input_box.send_keys(modifier_key + "A")
        time.sleep(.1)
        input_box.send_keys(query)
        field_id2 = f"item_sub_keyword{i+1}_1"
        input_box2 = driver.find_element(By.ID, field_id2)
        input_box2.send_keys(modifier_key + "A")
        time.sleep(.1)
        input_box2.send_keys(modifier_key + "A")
        time.sleep(.1)
        input_box2.send_keys(query)
        # print(f"입력 완료: {field_id} -> {keyword}")


def extract_relative_trend_score(driver):
    """
    라인차트 데이터 포인트를 추출
    max cy: 469, min cy: 2
    Args:
        driver: Selenium WebDriver 객체
    
    Returns:
        list: 각 데이터 포인트의 cy 좌표를 통해 트렌드 점수를 산출
        트렌드 점수 산출 방법: baseline 좌표 합을 기준으로 한 상대값 
    """
    # 해당 차트의 모든 circle 요소 가져오기
    # chart_class_list = ["bb-target-data" + str(i) for i in range(5)]
    chart_class_list = ["bb-target-data" + str(i) for i in range(2)]
    trend_score = []
    for chart_class in chart_class_list:
        circles = driver.find_elements(By.CSS_SELECTOR, f"g.{chart_class} circle")
        data_points = []
        for circle in circles:
            cy = circle.get_attribute("cy")  # cy 속성 추출
            if cy:  # cy 값이 존재하는 경우만 추가
                data_points.append(469 - float(cy))
        trend_score.append(sum(data_points))
    # print(trend_score)
    # trend_score_relative = [ts / trend_score[0] for ts in trend_score[1:]]
    trend_score_relative = trend_score[1] / trend_score[0]
    return trend_score_relative


def run_fetch(keyword, base_keyword):
    # 네이버 트렌드 데이터 수집 진행
    # 품목 리스트
    # item_name_list = "농어, 광어, 대게, 연어, 우럭, 참돔, 방어".split(', ')

    # 1. URL 접속
    driver = webdriver.Chrome()

    url = "https://datalab.naver.com/"
    driver.get(url)                 # URL로 이동

    # 기본 옵션 설정

    # # 범위 설정 (월 기준)
    # select_dropdown_option(driver, "timeDimensionTitle", "//li[contains(@class, '_item_month')]/a")
    # # 범위 설정 (주 기준)
    # select_dropdown_option(driver, "timeDimensionTitle", "//li[contains(@class, '_item_week')]/a")
    # 범위 설정 (일 기준)
    select_dropdown_option(driver, "timeDimensionTitle", "//li[contains(@class, '_item_date')]/a")
    time.sleep(1)

    # 시작 연월 설정
    select_dropdown_option(driver, "startYear", "//div[@id='startYearDiv']//li[contains(@class, '_item_2016')]/a")
    select_dropdown_option(driver, "startMonth", "//div[@id='startMonthDiv']//li[contains(@class, '_item_01')]/a")
    select_dropdown_option(driver, "startDay", "//div[@id='startDayDiv']//li[contains(@class, '_item_01')]/a")
    time.sleep(1)

    # 종료 연월 설정
    select_dropdown_option(driver, "endYear", "//div[@id='endYearDiv']//li[contains(@class, '_item_2025')]/a")
    select_dropdown_option(driver, "endMonth", "//div[@id='endMonthDiv']//li[contains(@class, '_item_01')]/a")
    select_dropdown_option(driver, "endDay", "//div[@id='endDayDiv']//li[contains(@class, '_item_29')]/a")
    time.sleep(1)

    # 연령 체크박스 정보
    age_info = {
        '06_12': "item_age_1",
        '13_18': "item_age_2",
        '19_24': "item_age_3",
        '25_29': "item_age_4",
        '30_34': "item_age_5",
        '35_39': "item_age_6",
        '40_44': "item_age_7",
        '45_49': "item_age_8",
        '50_54': "item_age_9",
        '55_59': "item_age_10",
        '60_80': "item_age_11",
    }

    trend_data = []
    # for item in item_name_list:
    for age in age_info:
        for uncheck in age_info.values():  # 체크박스 초기화
            toggle_checkbox(driver, uncheck, check=False)
        toggle_checkbox(driver, age_info[age], check=True)
        # for gt in game_trend_list:
        #     input_keywords(driver, gt)  # 키워드 입력

        # if (age, item) in [(t['age'], t['name']) for t in trend_data]:
        #     continue
        input_keyword(driver, baseline_keyword=base_keyword, input_keyword=keyword+","+base_keyword)  # 키워드 입력
        search_btn = driver.find_element(
            By.CSS_SELECTOR,
            "#content > div._search_trend_wrapper > div.keyword_trend > div > div > form > fieldset > a, #content > div.section_keyword > div.keyword_trend > div.section_step > div.com_box_inner > form > fieldset > a"
        )
        search_btn.click()  # 조회버튼 클릭
        print(age, keyword, end="/")
        # print(gt)
        time.sleep(2)
        # trend_score = extract_relative_trend_score(driver)
        chart_class_list = ["bb-target-data" + str(i) for i in range(2)]
        score_tmp = []
        for chart_class in chart_class_list:
            circles = driver.find_elements(By.CSS_SELECTOR, f"g.{chart_class} circle")
            data_points = []
            for circle in circles:
                cy = circle.get_attribute("cy")  # cy 속성 추출
                if cy:  # cy 값이 존재하는 경우만 추가
                    # data_points.append(469 - float(cy))
                    # for g, s in zip(gt, trend_score):
                    data_points.append(469 - float(cy))
            score_tmp.append(data_points)
        for i, s in enumerate(zip(*score_tmp)):
            trend_data.append({
                "idx": i,
                "age": age,
                "name": keyword,
                "score": s[1]/s[0]
            })
        print(len([t for t in trend_data if t["name"] == keyword and t["age"] == age]))
    return trend_data


def run_crawling():
    item_name_list = "농어, 광어, 대게, 연어, 우럭, 참돔, 방어".split(', ')
    today = time.strftime("%Y-%m-%d")

    for item in item_name_list:
        trend_data = run_fetch(item, "회")
        df = pd.DataFrame(trend_data)
        
        # 시작 날짜 설정
        start_date = pd.Timestamp("2016-01-01")

        # idx를 날짜로 변환
        df['date'] = start_date + pd.to_timedelta(df['idx'], unit='D')

        # 파일로 저장
        output_file = f"data/raw/nst_{item}_trend_{today}.csv"
        df.to_csv(output_file, index=False, encoding="utf-8")
        

if __name__ == "__main__":
    run_crawling()
