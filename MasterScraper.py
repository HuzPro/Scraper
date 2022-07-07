from pathlib import Path
from time import sleep
from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
        
        Title.append(str(soup.find_all("a", attrs={"target":"_blank", "href":True, "class":"text-base md:text-2xl text-adzuna-green-500 hover:underline"})[i].text).strip())
        tempList.append(str(soup.find_all("div", attrs={"class":"text-sm md:text-base xl:flex xl:flex-wrap"})[i].text).strip().partition("-"))
        Description.append(str(soup.find_all("span", attrs={"class":"max-snippet-height md:block md:overflow-hidden lg:h-auto lg:inline"})[i].text).strip())
        Link.append(str(soup.find_all("a", attrs={"class":"text-base md:text-2xl text-adzuna-green-500 hover:underline", "href":True, "target":"_blank"})[i]["href"]))
        Company.append(tempList[i][0])
        Location.append(tempList[i][2])
    return Title, Description, Link, Company, Location

page_Iter = 1

jobsLinkList, JobTitle, JobLink, JobCompany, JobLocation, JobTimePosted, JobDescription = [], [], [], [], [], [], []
FileHeader = ["Title", "Link", "Company", "Location", "Time Posted", "Description"]

#while True:
#    AI_overSeasJobsURL = "https://www.overseasjobs.com/job/search?keyword=Artificial%20Intelligence&Action=Search&country=US&location=&p="+str(page_Iter)
#    r_AI_OSJ = requests.get(AI_overSeasJobsURL)
#    if r_AI_OSJ.ok and page_Iter>=10: #was false after 2nd iter 2 times now
#        soup_AI_OSJ = BeautifulSoup(r_AI_OSJ.content, "html5lib")
#        JobTitle, JobLink, JobCompany, JobTimePosted, JobLocation = OSJ_jobToVariable(soup_AI_OSJ, JobTitle, JobLink, JobCompany, JobTimePosted, JobLocation)
#        print("Saved page"+str(page_Iter)+"'s data from OverSeasJobs.com")
#        page_Iter+=1
#    else:
#        print("Exited OverSeasJobs.com")
#        break
#
#page_Iter=1
#while True:
#    AI_AdzunaURL = "https://adzuna.com/search?ac_where=2&loc=151946&q=Artificial%20Intelligence&p="+str(page_Iter)
#    r_AI_ADZ = requests.get(AI_AdzunaURL)
#    if r_AI_ADZ.ok and page_Iter<=10:
#        soup_AI_ADZ = BeautifulSoup(r_AI_ADZ.content, "html5lib")
#        JobTitle, JobDescription, JobLink, JobCompany, JobLocation = ADZ_jobToVariable(soup_AI_ADZ, JobTitle, JobDescription, JobLink, JobCompany, JobLocation)
#        print("Saved page"+str(page_Iter)+"'s data from Adzuna.com")
#        page_Iter+=1
#    else:
#        print("Exited Adzuna.com")
#        break

RPK_AIE_Link = 'https://www.rozee.pk/job/jsearch/q/Artificial%20Intelligence%20Engineer/stype/title'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument("--headless")
browser = webdriver.Chrome(executable_path="C:\\Users\\DSU\\Downloads\\chromedriver.exe", options=options)
browser.get(RPK_AIE_Link)
wait = WebDriverWait(browser, 1)
r_RPK_AIE = browser.page_source
soup_RPK_AIE = BeautifulSoup(r_RPK_AIE, "html.parser")



aList = []
makelink = soup_RPK_AIE.find_all("div", attrs={"class":"jobt float-left"})
for x in range(len(makelink)):
    jobsLinkList.append(makelink[x].find("a", attrs={"href":True})['href'])
for link in jobsLinkList:
    r_job = requests.get("https:"+link)
    soup_job = BeautifulSoup(r_job.content, "html5lib")
    #JobTitle.append(str(soup_job.find_all("h1", attrs={"class":"jtitle font24 text-dark"})[0].text).strip())
    #JobLink.append(str("https:"+link))
    #JobCompany.append(str(soup_job.find_all("h2", attrs={"class":"cname im1 font18 mr5 text-dark"})[0].text).strip())
    tempvar = []
    #tempvar.append(str(soup_job.find_all("h4", attrs={"class":"lh1 cname im2 font18 text-dark d-flex align-items-center"})[0].text).partition(","))
    #JobLocation.append(str(tempvar[0][0]).strip() + ", " + str(tempvar[0][2]).strip())
    #tempvar.append(str(soup_job.find_all("div", attrs={"class":"jblk col-pl-0"})[0].text).replace("Job Details","").replace("\n","").expandtabs().strip().split(" "))
    tempvar.append(soup_job.find("div", attrs={"class":"jblk col-pl-0"}).find_all("div", attrs={"class":"row"})[0].text)
    print(tempvar)


#with open("htmltestsfile.html", "w", encoding="utf-8") as f:
#    f.write(aList[0]+aList[1])

#ws.append(FileHeader)
#for col in ws.iter_cols(min_row=2, max_row=len(JobTitle)+1, max_col=len(FileHeader)):
#    for j, cell in enumerate(col):
#        try:
#            if cell.column == 1 and JobTitle[j]: cell.value = JobTitle[j]
#            if cell.column == 2 and JobCompany[j]: cell.value = JobCompany[j]
#            if cell.column == 3 and JobLocation[j]: cell.value = JobLocation[j]
#            if cell.column == 4 and JobTimePosted[j]: cell.value = JobTimePosted[j]
#            if cell.column == 5 and JobLink[j]: cell.value = JobLink[j]
#            if cell.column == 6 and JobDescription[j]: cell.value = JobDescription[j]
#        except IndexError: pass
#
#wb.save(progName+".xlsx")
