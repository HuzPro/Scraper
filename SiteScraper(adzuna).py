from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

progName = "AI Jobs(adzuna)"
wb = Workbook()
ws = wb.active
ws.title = progName

AISearchURL = "https://www.adzuna.com/search?q=Artificial%20Intelligence&loc=151946&ac_where=1"

r = requests.get(AISearchURL)
soup = BeautifulSoup(r.content, "html5lib")

numOfJobs = 10
jobTitles = []
jobCompany = []
jobLocation = []
jobDescription = []
jobLink = []
tempList = []

test = soup.find("a", attrs={})


for i in range(numOfJobs):
    jobTitles.append(str(soup.find_all("a", attrs={"target":"_blank", "href":True, "class":"text-base md:text-2xl text-adzuna-green-500 hover:underline"})[i].text).replace("\n                    ","").replace("\n                ",""))
    tempList.append(str(soup.find_all("div", attrs={"class":"text-sm md:text-base xl:flex xl:flex-wrap"})[i].text).replace("\n            \n            \n            \n            ","").replace("          \n          \n              ","").replace("\n          \n\n        ","").partition("-"))
    jobDescription.append(str(soup.find_all("span", attrs={"class":"max-snippet-height md:block md:overflow-hidden lg:h-auto lg:inline"})[i].text).replace("\n            ","").replace("\n            ",""))
    jobLink.append(str(soup.find_all("a", attrs={"class":"text-base md:text-2xl text-adzuna-green-500 hover:underline", "href":True, "target":"_blank"})[i]["href"]))
    jobCompany.append(tempList[i][0])
    jobLocation.append(tempList[i][2])


fileHeaders = ["Title", "Company", "Location", "Description", "Link"]
ws.append(fileHeaders)
for col in ws.iter_cols(min_row=2, max_row=numOfJobs+1, max_col=5):
    for j, cell in enumerate(col):
        if cell.column == 1: cell.value = jobTitles[j]
        if cell.column == 2: cell.value = jobCompany[j]
        if cell.column == 3: cell.value = jobLocation[j]
        if cell.column == 4: cell.value = jobDescription[j]
        if cell.column == 5: cell.value = jobLink[j]

wb.save(progName+".xlsx")
