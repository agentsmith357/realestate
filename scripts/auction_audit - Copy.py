from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import re, os, requests
import pandas as pd
from bs4 import BeautifulSoup
#### below is how to launch headless selenium and download files
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest, time, re
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime, timedelta 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import xlsxwriter

path = os.path.dirname(os.path.abspath(__file__)) + "\\"
chrome_options = Options()

#chrome_options.add_argument("--headless")  
prefs = {'download.default_directory' : path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False }

os.chdir(os.path.dirname(__file__))

chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
driver = webdriver.Chrome(options=chrome_options)
print("Loaded chrome options.")
driver.implicitly_wait(30)
driver.set_page_load_timeout(30)
#driver.get("http://www.google.com/")

all_data = []
driver.get("https://hillsborough.realforeclose.com/index.cfm?resetcfcobjs=1")
driver.find_element(By.ID, "LogName").send_keys("shoother")
driver.find_element(By.ID, "LogPass").send_keys("zxzxzxA1!")
driver.find_element(By.ID, "LogButton").click()
driver.find_element(By.ID, "BNOTACC").click()
sleep(1)
driver.find_element(By.ID, "BNOTACC").click()
sleep(1)
driver.find_element(By.ID, "BNOTACC").click()
sleep(1)

#driver.get("https://google.com")

day_count =0
loc = os.path.dirname(os.path.abspath(__file__)) + "\\"

workbook = xlsxwriter.Workbook(loc + 'auction_audit2.xlsx') 
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'date') 
worksheet.write(0, 1, 'auction_status') 
worksheet.write(0, 2, 'auction_type') 
worksheet.write(0, 3, 'case') 
worksheet.write(0, 4, 'final_judgement') 
worksheet.write(0, 5, 'parcel_id') 
worksheet.write(0, 6, 'address') 
worksheet.write(0, 7, 'assessed_value') 
worksheet.write(0, 8, 'max_bid') 

t =0
auction_status = "UNKNOWN"
auction_type = "UNKNOWN"
case = "UNKONWN"
final_judgement = "UNKNOWN"
parcel_id = "UNKNOWN"
address = "UNKNOWN"
assessed_value = "UNKNOWN"
max_bid = "UNKNOWN"
lines = []


captured = []
temp_captured =[]
start = datetime.strptime("08/06/2023","%m/%d/%Y")
end = datetime.strptime("11/01/2023","%m/%d/%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
for single_date in date_generated:
    print(single_date.strftime("%m/%d/%Y"))        
    driver.get("https://hillsborough.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=DAYLIST&AUCTIONDATE="+single_date.strftime("%m/%d/%Y"))
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "Area_W"))
    # )
    sleep(1)
    body = driver.find_element(By.ID, 'MAIN_TBL_CONTENT')
    new_body = body.text.replace('\n', ' ~ ')
    result = re.split(r'\~',new_body)
    #result2 = BeautifulSoup(driver.page_source, 'html.parser')
    #result = [quote_tag.text for quote_tag in result2.find_all("MAIN_TBL_CONTENT")]

    status1 = 0
    status1count = 0
    address_start = 0 
    address_capture = []
    finished = 0
    for temp in result:
        # start auction status
        if status1 == 1:
            status1count = 1
        if re.search(r'Auction Status|Auction Starts',temp,re.IGNORECASE):
            status1 = 1
            
        if status1 == 1 and status1count == 1:
            auction_status = temp
            status1 = 0
            status1count = 0
        # end  auction status

        # start auction type
        if re.search(r'Auction Type\:\s+(.+?)$',temp,re.IGNORECASE):
            auction_type = re.search(r'Auction Type\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end auction type

        # start case 
        if re.search(r'Case \#\:\s+(.+?)$',temp,re.IGNORECASE):
            case = re.search(r'Case \#\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end case 

        # start judgement 
        if re.search(r'Final Judgment Amount\:\s+(.+?)$',temp,re.IGNORECASE):
            final_judgement = re.search(r'Final Judgment Amount\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end judgement 
        
        # start parcel_id 
        if re.search(r'Parcel ID\:\s+(.+?)$',temp,re.IGNORECASE):
            parcel_id = re.search(r'Parcel ID\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end parcel_id 

         # start parcel_id 
        if address_start == 1:
            if re.search(r'Assessed Value\:',temp,re.IGNORECASE):
                address_start =0
            else:
                address_capture.append(temp)
        if re.search(r'Property Address\:',temp,re.IGNORECASE):
            address_capture.append(re.search(r'Property Address\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0])
            address_start = 1

        # end parcel_id 
               

        # start parcel_id 
        if re.search(r'Assessed Value\:\s+(.+?)$',temp,re.IGNORECASE):
            assessed_value = re.search(r'Assessed Value\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end parcel_id 

        # start max_bid 
        if re.search(r'Max Bid\:\s+(.+?)$',temp,re.IGNORECASE):
            max_bid = re.search(r'Max Bid\:\s+(.+?)$',temp,re.IGNORECASE).groups(1)[0]
        # end max_bid 
            address = ' '.join(address_capture)
            temp_captured = {"Auction_Status":auction_status,
            "Auction_type":auction_type,
            "Case":case,
            "Judgement":final_judgement,
            "parcel_id":parcel_id,
            "address":address,
            "assessed_value":assessed_value,
            "max_bid":max_bid,
            "date":single_date.strftime("%m/%d/%Y")
            }
            captured.append(temp_captured)
            finished = 0
            auction_status = "UNKNOWN"
            auction_type = "UNKNOWN"
            case = "UNKONWN"
            final_judgement = "UNKNOWN"
            parcel_id = "UNKNOWN"
            address = "UNKNOWN"
            assessed_value = "UNKNOWN"
            max_bid = "UNKNOWN"
            address_capture = []
    
print("writing to disk...")
for line in captured:
    t+=1
    worksheet.write(t, 0, line["date"])
    worksheet.write(t, 1, line["Auction_Status"])
    worksheet.write(t, 2, line["Auction_type"])
    worksheet.write(t, 3, line["Case"])
    worksheet.write(t, 4, line["Judgement"])
    worksheet.write(t, 5, line["parcel_id"])
    worksheet.write(t, 6, line["address"])
    worksheet.write(t, 7, line["assessed_value"])
    worksheet.write(t, 8, line["max_bid"])

workbook.close()
print("done.")

