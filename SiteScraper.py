from bs4 import BeautifulSoup, Tag
import requests
from openpyxl import Workbook, load_workbook

progName = "Artificial Intelligence Jobs"
wb = Workbook()
ws = wb.active
ws.title = progName

AISearchURL = "https://www.overseasjobs.com/job/search?Action=Search&keyword=Artificial%20Intelligence&country=US&location="
AISearchURL2 = "https://www.adzuna.com/search?q=Artificial%20Intelligence&loc=151946&ac_where=1"

r = requests.get(AISearchURL)
soup = BeautifulSoup(r.content, "html5lib")

numberOfJobs = 20


jobTitles = soup.find_all("a", attrs={"data-job-source":True})
#jobEmployer = soup.find_all("a", attrs={"title":"Job Search", "href":True} )
jobEmployer = soup.find_all("a", attrs={"href":True, "target":"_blank"})


for item in jobEmployer:
    print(str(item['href'])+"\n")

jobTitleList = []
jobEmployerList = []
fileHeaders = []


#print(len(jobTitles), len(jobEmployer))
#for i in range(numberOfJobs):
#    jobTitleList.append(str(jobTitles[i]['title']))
#    print(i ,jobEmployer[i]['href'])
#    jobEmployerList.append(str(jobEmployer[i]['href']))

#print(jobEmployerList)
#
#fileHeaders.append("Job Titles")
#ws.append(fileHeaders)
#
#for i, row in enumerate(ws.iter_rows(min_row=1, max_row=numberOfJobs, max_col=1)):
#    for cell in row:
#        cell.value = jobTitleList[i]
#
#wb.save(progName+".xlsx")
