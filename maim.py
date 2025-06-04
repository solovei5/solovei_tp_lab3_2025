import requests
from bs4 import BeautifulSoup as BS

url = requests.get("https://data.uoi.ua/contest/uoi/2025/results")

html = BS(url.content, features="html.parser")

table = html.select("body > div > center > div > table > tbody > tr")
thead = html.select("body > div > center > div > table > thead > tr > th")

data = []
row = []
for th in thead:
    row.append(th.text)
data.append(row)

for tr in table:
    row = []
    for td in tr.select("td"):
        if td.text.isdecimal():
            row.append(int(td.text))
        else:
            row.append(td.text)
    data.append(row)


with open("results.csv", "w", encoding="utf-8") as file:
    for row in data:
        file.write(",".join([str(x) for x in row]) + "\n")


data_region = {}
winners_1 = []
winners_2 = []
winners_3 = []
winners_11grade = []
participants_region = {}

for row in data[1:]:
    region = row[2]
    grade = str(row[5])
    place = row[13]


    if region not in participants_region:
        participants_region[region] = 0
    participants_region[region] += 1

    if region not in data_region:
        data_region[region] = 0

    if place == 'I':
        data_region[region] += 1
        winners_1.append(row)
    if place == 'II':
        winners_2.append(row)
    if place == 'III':
        winners_3.append(row)
    if place in ['I', 'II', 'III'] and grade == '11':
        winners_11grade.append(row)


max_winners_region = max(data_region, key=data_region.get)
prizer_count = {}
for row in data[1:]:
    region = row[2]
    place = row[13]
    if place in ['I', 'II', 'III']:
        if region not in prizer_count:
            prizer_count[region] = 0
        prizer_count[region] += 1
max_prizer_region = max(prizer_count, key=prizer_count.get)


with open("analysis.txt", "w", encoding="utf-8") as f:
    f.write("Область з найбільшою кількістю переможців (I місце): " + max_winners_region + "\n")
    f.write("Область з найбільшою кількістю призерів (I-III місця): " + max_prizer_region + "\n\n")

    f.write("Переможці (I місце):\n")
    for row in winners_1:
        f.write(row[1] + " (" + row[2] + ")\n")

    f.write("\nПризери (II місце):\n")
    for row in winners_2:
        f.write(row[1] + " (" + row[2] + ")\n")

    f.write("\nПризери (III місце):\n")
    for row in winners_3:
        f.write(row[1] + " (" + row[2] + ")\n")

    f.write("\nПризери та переможці 11 класу:\n")
    for row in winners_11grade:
        f.write(row[1] + " (" + row[2] + ", " + str(row[5]) + " клас)\n")

    f.write("\nСтатистика по регіонах:\n")
    for reg in participants_region:
        f.write(reg + ": " + str(participants_region[reg]) + " учасників\n")
