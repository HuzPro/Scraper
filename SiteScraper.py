from bs4 import BeautifulSoup   #Beautiful Soup 4: Used to Parse raw HTML
import requests                 #Requests: Used to send requests to websites
from openpyxl import Workbook   #OpenPyxl: Used for excel file manipulation

progName = "Artificial Intelligence Jobs"
wb = Workbook()
ws = wb.active  #To work on the active worksheet
ws.title = progName #Worksheet title = program name

AISearchURL = "https://www.overseasjobs.com/job/search?keyword=Artificial%20Intelligence&Action=Search&country=US&location=&p=1"

r = requests.get(AISearchURL)   #getting the html from the link
soup = BeautifulSoup(r.content, "html5lib") #Parsing the html (making html useable/accessable)

numberOfJobs = 20   #The amount of jobs I want to record (for this website 20 is max jobs displayed on one page)


#Scraping the data using html tags and their attributes
jobTitles = soup.find_all("a", attrs={"data-job-source":True})
jobEmployer = soup.find_all("a", attrs={"href":True, "target":"_blank"})
jobLocation = soup.find_all("div", attrs={"class":"job-location"})
jobPosted = soup.find_all("footer",limit=20)


#Making list to store information from the raw scraped values
jobPostedList = []
jobTitleList = []
jobEmployerList = []
jobLinkList = []
jobLocationList = []

#What goes on the top of the excel file
fileHeaders = ["Job Titles", "Time posted/Posted by", "Job Location", "Link Of Job Source", "Link Of Job Post"]

#Appending to respective lists from the raw values scraped (and formatting)
for i in range(numberOfJobs*2): #The jobEmployer variable had both the job's links and employer's link so the number of links are 40. Alternatively storing values.
    if i%2==0:
        jobLinkList.append(str(jobEmployer[i]['href']))
    else:
        jobEmployerList.append(str(jobEmployer[i]['href']))

for i in range(numberOfJobs):   #All of these have 20 values. Adding the values to list to export to excel
    jobTitleList.append(str(jobTitles[i]['title']))
    jobLocationList.append(str(jobLocation[i].string))
    jobPostedList.append(str(jobPosted[i].string).replace("Posted: ","").replace("Posted on: ", "").replace("Posted on ", "").replace("\n","").replace("\t\t",""))
    if jobLocationList[i] == "None": jobLocationList[i] = "NA"
    



#Storing data and values into excel file
ws.append(fileHeaders)
for col in ws.iter_cols(min_row=2, max_row=numberOfJobs+1, max_col=5):    #Starting at row 2 because row 1 has the headers
    for j, cell in enumerate(col):  #Itrating to store specific values from list into cells
        if cell.column == 1: cell.value = jobTitleList[j]
        if cell.column == 2: cell.value = jobPostedList[j]
        if cell.column == 3: cell.value = jobLocationList[j]
        if cell.column == 4: cell.value = jobEmployerList[j]
        if cell.column == 5: cell.value = jobLinkList[j]

wb.save(progName+".xlsx")   #Saving excel file
