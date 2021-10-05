from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SERACH_BAR_ID = "query"
SEARCH_OPTIONS_ID = "basic-bools"
SEARCH_RESULTS_ID = "search-results"
driver = webdriver.Chrome(ChromeDriverManager().install())

def FindStuffs(term:str, county:str, city:str):
    URL = f"https://{county}.craigslist.org/"
    driver.get(URL)
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, SERACH_BAR_ID)))
    search_bar.send_keys(f"{city} {term}")
    search_bar.send_keys(Keys.ENTER)
    options = driver.find_element_by_id(SEARCH_OPTIONS_ID)
    lists = options.find_elements_by_tag_name("li")
    print(options)
    results = driver.find_element_by_id(SEARCH_RESULTS_ID)
    print(results)
    
FindStuffs("car", "orangecounty", "long beach")