from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

progName = "AI Jobs(Master File)"
wb = Workbook()
ws = wb.active
ws.title = progName

def OSJ_jobToVariable(soup ,Title, Link, Company, TimePosted, Location):
    numOfJobs_OSJ = 20
    tempList = []
    for i in range(numOfJobs_OSJ*2):
        try:
            if i%2==0:
                Link.append(str(soup.find_all("a", attrs={"href":True, "target":"_blank"})[i]['href']))
        except IndexError: pass
    for i in range(numOfJobs_OSJ):
        try:
            Title.append(str(soup.find_all("a", attrs={"data-job-source":True})[i]['title']))
            Location.append(str(soup.find_all("div", attrs={"class":"job-location"})[i].string))
            tempList.append(str(soup.find_all("footer",limit=20)[i].string).replace("Posted: ","").replace("Posted on: ", "").replace("Posted on ", "").replace("\n","").replace("\t\t","").partition("by "))
            TimePosted.append(tempList[i][0])
            Company.append(tempList[i][2])
            if Location[i] == "None": Location[i] = "NA"
            if Title[i] == "None": Title[i] = "NA"
            if JobLocation[i] == "None": JobLocation[i] = "NA"
            if TimePosted[i] == "None": TimePosted[i] = "NA"
            if Link[i] == "None": Link[i] = "NA"
        except IndexError: pass
    return Title, Link, Company, TimePosted, Location

def ADZ_jobToVariable(soup, Title, Description, Link, Company, Location):
    numOfJobs_ADZ = 10
    tempList = []
    for i in range(numOfJobs_ADZ):
        
        Title.append(str(soup.find_all("a", attrs={"target":"_blank", "href":True, "class":"text-base md:text-2xl text-adzuna-green-500 hover:underline"})[i].text).replace("\n                    ","").replace("\n                ",""))
        tempList.append(str(soup.find_all("div", attrs={"class":"text-sm md:text-base xl:flex xl:flex-wrap"})[i].text).replace("\n            \n            \n            \n            ","").replace("          \n          \n              ","").replace("\n          \n\n        ","").partition("-"))
        Description.append(str(soup.find_all("span", attrs={"class":"max-snippet-height md:block md:overflow-hidden lg:h-auto lg:inline"})[i].text).replace("\n            ","").replace("\n            ",""))
        Link.append(str(soup.find_all("a", attrs={"class":"text-base md:text-2xl text-adzuna-green-500 hover:underline", "href":True, "target":"_blank"})[i]["href"]))
        Company.append(tempList[i][0])
        Location.append(tempList[i][2])
    return Title, Description, Link, Company, Location

page_Iter = 1

JobTitle, JobLink, JobCompany, JobLocation, JobTimePosted, JobDescription = [], [], [], [], [], []
FileHeader = ["Title", "Company", "Location", "Time Posted", "Link", "Description"]








while True:
    
    AI_overSeasJobsURL = "https://www.overseasjobs.com/job/search?keyword=Artificial%20Intelligence&Action=Search&country=US&location=&p="+str(page_Iter)
    r_AI_OSJ = requests.get(AI_overSeasJobsURL)
    if requests.Response.ok:
        soup_AI_OSJ = BeautifulSoup(r_AI_OSJ.content, "html5lib")
        JobTitle, JobLink, JobCompany, JobTimePosted, JobLocation = OSJ_jobToVariable(soup_AI_OSJ, JobTitle, JobLink, JobCompany, JobTimePosted, JobLocation)
        page_Iter+=1
    else: break

while True:
    AI_AdzunaURL = "https://www.adzuna.com/search?q=Artificial%20Intelligence&loc=151946&ac_where="+str(page_Iter)
    r_AI_ADZ = requests.get(AI_AdzunaURL)
    if requests.Response.ok or page_Iter==20:
        soup_AI_ADZ = BeautifulSoup(r_AI_ADZ.content, "html5lib")
        JobTitle, JobDescription, JobLink, JobCompany, JobLocation = ADZ_jobToVariable(soup_AI_ADZ, JobTitle, JobDescription, JobLink, JobCompany, JobLocation)
        page_Iter+=1
    else: break



ws.append(FileHeader)
for col in ws.iter_cols(min_row=2, max_row=len(JobTitle)+1, max_col=len(FileHeader)):
    for j, cell in enumerate(col):
        try:
            if cell.column == 1 and JobTitle[j]: cell.value = JobTitle[j]
            if cell.column == 2 and JobCompany[j]: cell.value = JobCompany[j]
            if cell.column == 3 and JobLocation[j]: cell.value = JobLocation[j]
            if cell.column == 4 and JobTimePosted[j]: cell.value = JobTimePosted[j]
            if cell.column == 5 and JobLink[j]: cell.value = JobLink[j]
            if cell.column == 6 and JobDescription[j]: cell.value = JobDescription[j]
        except IndexError: pass

wb.save(progName+".xlsx")
