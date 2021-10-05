from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SERACH_BAR_ID = "query"
SEARCH_OPTIONS_ID = "basic-bools"
CHECKBOX_POSTED_TODAY = "postedToday"
CHECKBOX_SEARCH_NEARBY = "searchNearby"
RESULT_LIST_ID = "search-results"
ROW_CLASS_NAME = "result-row"
PRICE_TAG_CLASS_NAME = "result-price"
driver = webdriver.Chrome(ChromeDriverManager().install())

def FindTodayPrices(term:str, city:str):
    results = []

    URL = f"https://craigslist.org/"
    driver.get(URL)
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, SERACH_BAR_ID)))
    search_bar.send_keys(f"{city} {term}")
    search_bar.send_keys(Keys.ENTER)
    options = driver.find_element_by_id(SEARCH_OPTIONS_ID)
    checkbox_posted_today = options.find_element_by_name(CHECKBOX_POSTED_TODAY)
    checkbox_posted_today.click()
    # options = driver.find_element_by_id(SEARCH_OPTIONS_ID)
    # checkbox_search_nearby = options.find_element_by_name(CHECKBOX_SEARCH_NEARBY)
    # checkbox_search_nearby.click()
    lists = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, RESULT_LIST_ID)))
    h4 = lists.find_element_by_tag_name("h4")
    if h4:
        driver.execute_script("arguments[0].setAttribute('class','result-row')", h4)
    rows = lists.find_elements_by_class_name(ROW_CLASS_NAME)
    
    for r in rows:
        if r.tag_name == "h4": break
        results.append(r.find_element_by_class_name(PRICE_TAG_CLASS_NAME).text)
    return results

term = "rent"
city = "long beach"
    
r = FindTodayPrices(term, city)
print(r)