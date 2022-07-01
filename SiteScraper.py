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

print(len(jobEmployer))

jobTitleList = []
jobEmployerList = []
jobLinkList = []
fileHeaders = ["Job Titles", "Link Of Employer", "Link Of Job"]


for i in range(numberOfJobs*2):
    if i%2==0:
        jobLinkList.append(str(jobEmployer[i]['href']))
    else:
        jobEmployerList.append(str(jobEmployer[i]['href']))

for i in range(numberOfJobs):
    jobTitleList.append(str(jobTitles[i]['title']))




ws.append(fileHeaders)

for i, row in enumerate(ws.iter_rows(min_row=1, max_row=numberOfJobs, max_col=3)):
    for cell in row:
        cell.value = jobTitleList[i]
        cell.value = jobEmployerList[i]
        cell.value = jobLinkList[i]

wb.save(progName+".xlsx")
