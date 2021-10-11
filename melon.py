from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import csv
import os

def saveCSV(rows):
    PARENT_DIR = f"{os.path.abspath(os.getcwd())}/static/uploads"
    os.makedirs(PARENT_DIR)
    with open(f"{PARENT_DIR}/melon.csv", 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['rank', 'title', "artist", "cover"]
        writer = csv.DictWriter(csvfile, delimiter=' ', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def scrap_asong(song):
    rank = ""
    title = ""
    artist = ""
    image_url = ""
    
    image_url = song.find_element_by_tag_name("img").get_attribute("src")
    rank = song.find_element_by_class_name("rank").text
    titleAndArtist = song.find_elements_by_class_name("ellipsis")
    
    title = titleAndArtist[0].find_element_by_tag_name("a").text
    artists = titleAndArtist[1].find_elements_by_tag_name("a")
    if len(artists) > 1: 
        for a in artists:
            if a.text != "": artist += (a.text + ", ")

    else: artist = titleAndArtist[1].find_elements_by_tag_name("a")[0].text
    return {"rank":rank.strip(), "title":title.strip(), "artist":artist.strip(), "cover": image_url.strip()}


def scrap_songs():
    URL = "https://www.melon.com/chart/index.htm"
    results = []
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    top50 = driver.find_elements_by_id("lst50")
    # top51to100 = driver.find_elements_by_id("lst100")

    for song in top50:
        asong = scrap_asong(song)
        results.append(asong)
    return results

r = scrap_songs()

saveCSV(r)