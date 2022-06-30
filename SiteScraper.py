from bs4 import BeautifulSoup
import requests

AISearchURL = "https://www.overseasjobs.com/job/search?Action=Search&keyword=Artificial%20Intelligence&country=US&location="
AISearchURL2 = "https://www.adzuna.com/search?q=Artificial%20Intelligence&loc=151946&ac_where=1"

result = requests.get(AISearchURL)

doc = BeautifulSoup(result.text, "html.parser")

jobTitles = doc.find_all("a", attrs={"data-job-source":True})
jobTitleList = []
for i in range(20):
    jobTitleList.append(str(jobTitles[i]['title']))

print(jobTitleList)
print(len(jobTitleList))
