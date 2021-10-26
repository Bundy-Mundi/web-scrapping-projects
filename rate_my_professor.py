from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import threading
import time

from bs4 import BeautifulSoup
import requests

sampleURL = "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2022/By_Subject/CHEM.html"

class CSULB:
    def __init__(self):
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = None
        self.result = []
        self.rmpUrl = "https://www.ratemyprofessors.com/"
        
        self.sid = "U2Nob29sLTE2Mg==" # sid of csu longbeach for Rate my professor
        self.school = "California State University Long Beach"
        self.col_class_id = 1
        self.col_prof_name = 9
        self.card_class = "TeacherCard__StyledTeacherCard-syjs0d-0"
        self.rating_class = "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2"
        self.name_class = "CardName__StyledCardName-sc-1gyrgim-0"
        self.major_class = "CardSchool__Department-sc-19lmz2k-0"
        self.feedbacks_class = "CardFeedback__CardFeedbackNumber-lq6nix-2"


    def extract_professor_names_and_classIds_bs4(self, html):
        results = []
        blocks = html.find_all(class_="courseBlock")
        for block in blocks:
            tds = block.find_all("td")
            results.append({"name": tds[self.col_prof_name].text, "classId": tds[self.col_class_id].text})
        return results

    '''
    def extract_professor_names_selenium(self, url:str):
        professors = []
        self.driver.get(url)
        blocks = self.driver.find_elements_by_class_name("courseBlock")
        for block in blocks:
            tds = block.find_elements_by_tag_name("td")
            name = tds[self.col].text
            professors.append(name)
        return professors
    '''
    
    def search_professor(self, prof:str, results:list):
        url = f"https://www.ratemyprofessors.com/search/teachers?query={prof}&sid={self.sid}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        cards = soup.find_all(class_=self.card_class)
        for c in cards:
            rating = c.find(class_=self.rating_class).text
            fullname = c.find(class_=self.name_class).text
            major = c.find(class_=self.major_class).text
            feedbacks = c.find_all(class_=self.feedbacks_class)
            would_take_again = feedbacks[0].text
            difficulty = feedbacks[1].text
            results.append({"rating": rating, "fullname": fullname, "major":major, "takeAgain": would_take_again, "difficulty": difficulty})
    
    def search_professors_in_page(self, url:str):
        results = []
        threads = []
        r = requests.get(url)
        html = BeautifulSoup(r.content, "html.parser")
        r = self.extract_professor_names_and_classIds_bs4(html)
        for element in r:
            x = threading.Thread(target=self.search_professor, args=(element["name"],results,))
            threads.append(x)
            x.start()
        for thread in threads:
            thread.join()
        return results

    def asyncFind(self, timing:int, tupleArg):
        return WebDriverWait(self.driver, timing).until(
            EC.presence_of_element_located(tupleArg)
        )

c = CSULB()
r = c.search_professors_in_page(sampleURL)
