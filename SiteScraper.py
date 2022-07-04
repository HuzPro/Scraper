from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

progName = "Artificial Intelligence Jobs"
wb = Workbook()
ws = wb.active
ws.title = progName

AISearchURL = "https://www.overseasjobs.com/job/search?keyword=Artificial%20Intelligence&Action=Search&country=US&location=&p=1"

r = requests.get(AISearchURL)
soup = BeautifulSoup(r.content, "html5lib")

numberOfJobs = 20


jobTitles = soup.find_all("a", attrs={"data-job-source":True})
jobEmployer = soup.find_all("a", attrs={"href":True, "target":"_blank"})
jobLocation = soup.find_all("div", attrs={"class":"job-location"})
jobPosted = soup.find_all("footer",limit=20)



jobPostedList = []
jobTitleList = []
jobEmployerList = []
jobLinkList = []
jobLocationList = []


fileHeaders = ["Job Titles", "Time posted/Posted by", "Job Location", "Link Of Job Source", "Link Of Job Post"]


for i in range(numberOfJobs*2):
    if i%2==0:
        jobLinkList.append(str(jobEmployer[i]['href']))
    else:
        jobEmployerList.append(str(jobEmployer[i]['href']))

for i in range(numberOfJobs):
    jobTitleList.append(str(jobTitles[i]['title']))
    jobLocationList.append(str(jobLocation[i].string))
    jobPostedList.append(str(jobPosted[i].string).replace("Posted: ","").replace("Posted on: ", "").replace("Posted on ", "").replace("\n","").replace("\t\t",""))
    if jobLocationList[i] == "None": jobLocationList[i] = "NA"
    




ws.append(fileHeaders)

for i, col in enumerate(ws.iter_cols(min_row=2, max_row=numberOfJobs+1, max_col=5)):
    for j, cell in enumerate(col):
        if cell.column == 1: cell.value = jobTitleList[j]
        if cell.column == 2: cell.value = jobPostedList[j]
        if cell.column == 3: cell.value = jobLocationList[j]
        if cell.column == 4: cell.value = jobEmployerList[j]
        if cell.column == 5: cell.value = jobLinkList[j]

wb.save(progName+".xlsx")
print("Done!!! :D")
