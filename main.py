from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://google.com")
s = driver.find_element_by_class_name("gLFyf")
s.send_keys("Hello world")
s.send_keys(Keys.ENTER)
el = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "g-blk")) # Seems like locator needs to be a tuple
print(el)

#driver.quit()