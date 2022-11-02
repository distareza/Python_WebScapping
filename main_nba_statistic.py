import requests
import re
from bs4 import BeautifulSoup
import csv

url = "https://www.nba.com/stats/"

response = requests.get(url)
response.raise_for_status()

web_content = BeautifulSoup(response.text, 'html.parser')

data = []
for div in web_content.findAll("div", re.compile("Block_block_*")):
    if div.findAll("h1", text="Players"):
        for div_section in div.findAll("div", re.compile("LeaderBoardCard_lbcWrapper_*")):
            section = div_section.findNext("h2").getText()
            for tbl_stats in div_section.findAll("tr"):
                tbl_section = tbl_stats.findAll("td")
                no = tbl_section[0].getText()
                name = tbl_section[1].findNext("a").getText()
                point = tbl_section[2].findNext("a").getText()
                print(f"{section},{name},{point}")
                data.append([section, name, point])

with open("nba_stats.csv","w", encoding="UTF8", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["section", "name", "point"])
    for row in data:
        writer.writerow(row)



