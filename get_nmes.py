import requests
import bs4
from bs4 import BeautifulSoup


link_part1 = "https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process&rptName=2&reportSelectMonth=" 
link_part2 = "&reportSelectYear=" 
link_part3 = "&nav"


year = 1900
month = 1
links = []

while year < 2021:
    if month < 13:
        print("adding link for month " + str(month) + " and year " + str(year))
        newlink = link_part1 + str(month) + link_part2 + str(year) + link_part3
        links.append((newlink, year))
        month += 1
    else:
        month = 1
        year +=1
        if year < 2021:
            print("adding link for month " + str(month) + " and year " + str(year))
            newlink = link_part1 + str(month) + link_part2 + str(year) + link_part3
            links.append((newlink, year))
            month += 1

year = 1900
nmes = {}
drug_dict = {}
while year < 2021:
    nmes[year] = []
    year +=1

for linktuple in links:
    print(str(linktuple))
    link = linktuple[0]
    year = linktuple[1]
    req = requests.get(link)
    soup = BeautifulSoup(req.content,"html.parser")
    for table in soup.find_all("table"):
        for tbody in table.find_all("tbody"):
            for tr in tbody.find_all("tr"):
                if tr.text.find("New Molecular Entity") != -1:
                    try:
                        text = tr.text.split("\n")
                        date = str(text[1])
                        drug = text[3]
                        priority = text[5]
                        company = text[6]
                        nmes[year].append(tr.text)
                        drug_dict[drug] = [("date", date),("company",company), ("priority",priority)]
                    except:
                        pass



numbers = []
for year in nmes.keys():
    print(str(year)+ ": " + str(len(nmes[year])))
    numbers.append((year, str(len(nmes[year]))))

for number in numbers:
    print(number)

for drug in drug_dict.keys():
    date = drug_dict[drug][0][1]
    company = drug_dict[drug][1][1]
    priority = drug_dict[drug][2][1]
    print(date +"\t" + company + "\t"+priority)
    with open("approvals.txt", "a") as writefile:
        writefile.write(drug + "\t" + date +"\t" + company + "\t"+priority+"\n")


