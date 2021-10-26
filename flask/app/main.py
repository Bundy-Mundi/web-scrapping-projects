from flask import Flask
from flask import request
from rate_my_professor import CSULB
from bs4 import BeautifulSoup
import requests
import json

YEAR = 2022
BOX_CLASS = "indexList"

app = Flask(__name__)
 
@app.route("/")
def home_view():
        c = CSULB()
        x = c.search_professors_in_page("http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2022/By_Subject/CHEM.html")
        return json.dumps(x)

@app.route("/spring")
def spring_view():
        html = ""
        BY_SUBJECT = "By_Subject"
        BY_COLLEGE = "By_College"
        BY_GE = "By_GE_Requirement"
        by = request.args.get("by")
        query = request.args.get("major")
        SET = {"subject":BY_SUBJECT, "college":BY_COLLEGE, "ge":BY_GE}
        if not by in SET:
                return "Wrong args"
        if by == "ge":
                query = request.args.get("area")
        if not query:
                return "Wrong args"
        url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_{YEAR}/{SET[by]}/{query}.html"
        print(url)
        c = CSULB()
        x = c.search_professors_in_page(url)
        return json.dumps(x)

@app.route("/fall")
def fall_view():
        url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Fall_{YEAR}/{SET[by]}/index.html"
        return url
