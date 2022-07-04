from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

progName = "AI Jobs(adzuna)"    #Name of the file that's going to be saved
wb = Workbook()
ws = wb.active
ws.title = progName             #Worksheet(the active sheet in excel)'s name assignment

AISearchURL = "https://www.adzuna.com/search?ac_where=2&loc=151946&q=Artificial%20Intelligence&p=1"

r = requests.get(AISearchURL)                   #Sending request to website for html
soup = BeautifulSoup(r.content, "html5lib")     #Parsing html (making it useable
#Variable initialization
numOfJobs = 10
jobTitles = []
jobCompany = []
jobLocation = []
jobDescription = []
jobLink = []
tempList = []

for i in range(numOfJobs):      #Loop to directly scrape the targetted elements and put the values into lists (whilst formatting them as well)
    jobTitles.append(str(soup.find_all("a", attrs={"target":"_blank", "href":True, "class":"text-base md:text-2xl text-adzuna-green-500 hover:underline"})[i].text).replace("\n                    ","").replace("\n                ",""))
    tempList.append(str(soup.find_all("div", attrs={"class":"text-sm md:text-base xl:flex xl:flex-wrap"})[i].text).replace("\n            \n            \n            \n            ","").replace("          \n          \n              ","").replace("\n          \n\n        ","").partition("-"))
    jobDescription.append(str(soup.find_all("span", attrs={"class":"max-snippet-height md:block md:overflow-hidden lg:h-auto lg:inline"})[i].text).replace("\n            ","").replace("\n            ",""))
    jobLink.append(str(soup.find_all("a", attrs={"class":"text-base md:text-2xl text-adzuna-green-500 hover:underline", "href":True, "target":"_blank"})[i]["href"]))
    jobCompany.append(tempList[i][0])
    jobLocation.append(tempList[i][2])


fileHeaders = ["Title", "Company", "Location", "Description", "Link"]   #What goes on the first row
ws.append(fileHeaders)                                                  #Putting it in the first row
for col in ws.iter_cols(min_row=2, max_row=numOfJobs+1, max_col=5):     #Exporting the values inthe scraped list variables to excel
    for j, cell in enumerate(col):
        if cell.column == 1: cell.value = jobTitles[j]
        if cell.column == 2: cell.value = jobCompany[j]
        if cell.column == 3: cell.value = jobLocation[j]
        if cell.column == 4: cell.value = jobDescription[j]
        if cell.column == 5: cell.value = jobLink[j]

wb.save(progName+".xlsx")   #Saving the excel file
