import requests
import re
from bs4 import BeautifulSoup
import csv

url = "https://www.audible.com/search?keywords=book&node=18573211011"


response = requests.get(url)
response.raise_for_status()

web_content = BeautifulSoup(response.text, 'html.parser')

data = []
for el in web_content.select("#product-list-a11y-skiplink-target > span > ul > li"):
    detail = el.select("div > div.bc-col-responsive.bc-spacing-top-none.bc-col-8 > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul")
    for li in detail:
        try:
            name = li.select("li > h3 > a")[0].getText()
        except:
            pass
        try:
            description = li.select("li.bc-list-item.subtitle > span")[0].getText()
        except:
            pass
        try:
            author = li.select("li.bc-list-item.authorLabel > span > a")[0].getText()
        except:
            pass
        try:
            narrator = li.select("li.bc-list-item.narratorLabel > span > a")[0].getText()
        except:
            pass
        try:
            length = li.select("li.bc-list-item.runtimeLabel > span")[0].getText()
            length = length.replace("Length:","").strip()
        except:
            pass
        try:
            release_date = li.select("li.bc-list-item.releaseDateLabel > span")[0].getText().strip()
            release_date = re.search(r"\d+-\d+-\d+", release_date).group()
        except:
            pass
        try:
            language = li.select("li.bc-list-item.languageLabel > span")[0].getText().strip()
            language = language.replace("Language:","").strip()
        except:
            pass
        try:
            rating = len(li.select("li.bc-list-item.ratingsLabel > div > span.full-review-star")) + len(li.select("li.bc-list-item.ratingsLabel > div > span.half-review-star"))/2
            rating = li.select("li.bc-list-item.ratingsLabel > span.bc-text.bc-pub-offscreen")[0].getText().strip()
        except:
            pass
        try:
            total_rating = li.select("li.bc-list-item.ratingsLabel > span.bc-text.bc-size-small.bc-color-secondary")[0].getText().strip()
        except:
            pass
        print(f"{name}, {description}, {author}, {narrator}, {length}, {release_date}, {language}, {rating}, {total_rating}")
        data.append([name, description, author, narrator, length, release_date, language, rating, total_rating])

with open("audible_static.csv","w", encoding="UTF8", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Description", "Author", "Narrator", "Length", "Release Date", "Language", "Rating", "Total Rating"])
    for row in data:
        writer.writerow(row)