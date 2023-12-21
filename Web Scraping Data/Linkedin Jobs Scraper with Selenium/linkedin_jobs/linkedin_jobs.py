#Import Packages

import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

#Use this Url and change city or role accordingly

url1='https://www.linkedin.com/jobs/search?keywords=Marketing%20Data%20Analyst&location=Berlin%2C%20Berlin%2C%20Germany&geoId=106967730&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get(url1)

#Find number of job listings

job_count_elements = driver.find_elements(By.CLASS_NAME, 'results-context-header__job-count')

if job_count_elements:
    y = job_count_elements[0].text
    print(y)
else:
    print("Job count element not found.")


n = pd.to_numeric(y)
print(n)

#Loop to scroll through all jobs and click on see more jobs button for infinite scrolling

i = 2
while i <= int((n+200)/25)+1: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    
    try:
        send=driver.find_element_by_xpath("//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)   
        time.sleep(3)
                
    except:
        pass
        time.sleep(5)

#Create empty lists for company name and job title

companyname= []
titlename= []

# Find company name and append it to the blank list

try:
    # Find company names using XPath
    company_elements = driver.find_elements(By.XPATH, "//h3[@class='base-search-card__title']")
    
    # Iterate over the elements and append to the list
    for company_element in company_elements:
        company = company_element.text
        companyname.append(company)

except Exception as e:
    print(f"An error occurred in the try block: {e}")

len(companyname)


# Find title name and append it to the blank list

try:
    # Find title names using XPath
    title_elements = driver.find_elements(By.XPATH, "//h3[@class='base-search-card__title']")
    
    # Iterate over the elements and append to the list
    for title_element in title_elements:
        title = title_element.text
        titlename.append(title)

except Exception as e:
    print(f"An error occurred in the try block: {e}")

len(titlename)

#Create dataframe for company name and title

companyfinal = pd.DataFrame(companyname,columns=["company"])
titlefinal = pd.DataFrame(titlename,columns=["title"])

#Join the two lists

x = companyfinal.join(titlefinal)
print(x)

#Save file in your directory

x.to_csv('linkedin.csv')

#Find job links and append it to a list

job_list = driver.find_elements(By.XPATH, "//a[@class='base-card__full-link']")
    
# Extract href attributes and append to the list
hrefList = []

for e in job_list:
        hrefList.append(e.get_attribute('href'))
        print(hrefList)


linklist = pd.DataFrame(hrefList,columns=["joblinks"])

linklist.to_csv('linkedinlinks.csv')

#Close the driver

driver.close()