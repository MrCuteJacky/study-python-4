from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

page = 0
while True:
    page += 1
    url = "https://tabelog.com/tw/rstLst/" + str(page) + "/?SrtT=rt"
    print("Start processing", url)
    try:
        output_file = open("output.txt", "a")
        response = urlopen(url)
        html = BeautifulSoup(response, features="html.parser")
        rst_list = html.select("li.list-rst")
        for rst in rst_list:
            ja = rst.find("small", class_="list-rst__name-ja").text
            en = rst.select_one("a.list-rst__name-main").text
            blog = rst.select_one("a.list-rst__name-main")["href"]
            rating_star = rst.select_one("i.c-rating__star").next.text
            rating_dinner = rst.select_one("span.c-rating__time--dinner").findNext("b", class_="c-rating__val").text
            rating_lunch = rst.select_one("span.c-rating__time--lunch").findNext("b", class_="c-rating__val").text
            print(rating_star, rating_dinner, rating_lunch, ja, en, blog)
            output_file.write(rating_star + "\t" + rating_dinner + "\t" + rating_lunch + "\t" + ja + "\t" + en + "\t" + blog + "\n")
    except HTTPError:
        output_file.close()
        print("Finish!!!")
        break
