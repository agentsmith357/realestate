from decimal import Decimal
from tqdm import tqdm
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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import xlsxwriter
def download_information():
    path = os.path.dirname(os.path.abspath(__file__)) + "\\"
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
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
    chrome_options.add_argument("--window-position=-10000,0")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    driver = webdriver.Chrome(options=chrome_options,service=service)
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
    driver.find_element(By.ID, "BNOTACC").click()
    sleep(1)

    day_count =0
    loc = os.path.dirname(os.path.abspath(__file__)) + "\\"

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
    #start = datetime.strptime("08/06/2023","%m/%d/%Y")
    #end = datetime.strptime("08/15/2023","%m/%d/%Y")
    end = timedelta(days = 60) 
    today = datetime.now()    
    start = timedelta(days=0) + today #2 days in the past to
    #start.strptime("%m/%d/%Y")
    end = timedelta(days=30) + today # 30 days into the future
    #end.strptime("%m/%d/%Y")
    older_than_3_days = today - timedelta(days=-3)
    print(f"Auditing from {start.strftime('%m/%d/%Y')} to {end.strftime('%m/%d/%Y')}")
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
        is_canceled = 0
        is_house_sold = 0
        watch_it = 0
        sold_amount = ''
        sold_to = ''
        caputure_sold_to =0
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

            if re.search(r'Auction Sold',temp,re.IGNORECASE):
                is_house_sold = 1
            if is_house_sold and len(sold_to) == 0:
                if caputure_sold_to == 1:
                    sold_to = temp
                    caputure_sold_to = 0
                if re.search(r'(\$.+?)$',temp,re.IGNORECASE):
                    sold_amount = re.search(r'(\$.+?)$',temp,re.IGNORECASE).groups()[0]
                if re.search(r'Sold To',temp,re.IGNORECASE):
                    caputure_sold_to = 1

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
            if not re.search(r'Auctions Closed or Canceled',temp,re.IGNORECASE):
                if re.search(r'Canceled',temp,re.IGNORECASE):
                    is_canceled = 1
                #parcel_id = re.search(r'Canceled',temp,re.IGNORECASE).groups(1)[0]
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
                auction_status =re.sub(r'\r|\n|^\s+|\s+$','',auction_status)
                auction_status =re.sub(r'\r|\n|^\s+|\s+$','',auction_status)
                case =re.sub(r'\r|\n|^\s+|\s+$','',case)
                final_judgement =re.sub(r'\r|\n|^\s+|\s+$','',final_judgement)
                parcel_id =re.sub(r'\r|\n|^\s+|\s+$','',parcel_id)
                address =re.sub(r'\r|\n|^\s+|\s+$','',address)
                assessed_value =re.sub(r'\r|\n|^\s+|\s+$','',assessed_value)
                max_bid =re.sub(r'\r|\n|^\s+|\s+$','',max_bid)
                if re.search(r'\$',final_judgement):
                    final_judgement = Decimal(re.sub(r'[^\d.]', '', final_judgement))
                    max_threshold =  Decimal("199999.99")
                    if max_threshold >=final_judgement:
                        watch_it = 1
                    else:
                        watch_it = 0
                else:
                    watch_it = 0

                if re.search(r'Canceled|Walked',auction_status,re.IGNORECASE):
                    watch_it = 0    
                sold_amount =re.sub(r'\r|\n|^\s+|\s+$','',sold_amount)
                sold_to =re.sub(r'\r|\n|^\s+|\s+$','',sold_to)

                address = ' '.join(address_capture)
                temp_captured = {"Auction_Status":auction_status,
                "Auction_type":auction_type,
                "Case":case,
                "Judgement":final_judgement,
                "parcel_id":parcel_id,
                "address":address,
                "assessed_value":assessed_value,
                "max_bid":max_bid,
                "date":single_date.strftime("%Y-%m-%d"),
                "is_canceled":is_canceled,
                "is_house_sold":is_house_sold,
                "amount_sold":sold_amount,
                "sold_to":sold_to,
                "is_watching":watch_it,

                }
                captured.append(temp_captured)
                finished = 0
                is_canceled = 0
                is_house_sold = 0
                watch_it = 0
                sold_amount = ''
                sold_to = ''
                caputure_sold_to =0
                auction_status = "UNKNOWN"
                auction_type = "UNKNOWN"
                case = "UNKONWN"
                final_judgement = "UNKNOWN"
                parcel_id = "UNKNOWN"
                address = "UNKNOWN"
                assessed_value = "UNKNOWN"
                max_bid = "UNKNOWN"
                address_capture = []
                
    return captured   


def save(houses):
    import pyodbc
    print("connecting to db...")
    conn = pyodbc.connect("""Driver={MySQL ODBC 8.0 Unicode Driver};
        Server=192.168.1.232;
        Database=realestate;
        UID=admin;
        PWD=zxzxzxA1!""")
    print("connected.")
    print("resetting watch list")
    with conn.cursor() as cur:
        cur.execute("""UPDATE houses
                SET is_watching = 0""")
    print("saving data to database...")
    for house in tqdm(houses):
        temp= None
        with conn.cursor() as cur:
            cur.execute("""SELECT 
            date
            ,auction_status
            ,auction_type
            ,case_number
            ,final_judgement
            ,parcel_id
            ,address
            ,assessed_value
            ,max_bid
            ,is_watching
            ,is_house_sold
            ,is_canceled
            FROM houses where
            date = ? and
            case_number = ? """,house['date'],house['Case'])
            temp = cur.fetchone()
        if temp is None:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO houses
                (date
                ,auction_status
                ,auction_type
                ,case_number
                ,final_judgement
                ,parcel_id
                ,address
                ,assessed_value
                ,max_bid
                ,is_house_sold
                ,is_canceled
                ,amount_sold
                ,sold_to
                ,is_watching)
                VALUES
                (?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?
                ,?)""",house["date"]
                ,house["Auction_Status"]
                ,house["Auction_type"]
                ,house["Case"]
                ,house["Judgement"]
                ,house["parcel_id"]
                ,house["address"]
                ,house["assessed_value"]
                ,house["max_bid"]
                ,house["is_house_sold"]
                ,house["is_canceled"] 
                ,house["amount_sold"]
                ,house["sold_to"]
                ,house["is_watching"]
                 )
        else:
            with conn.cursor() as cur:
                cur.execute("""UPDATE houses
                SET auction_status = ?
                ,auction_type = ?
                ,final_judgement = ?
                ,parcel_id = ?
                ,address= ?
                ,assessed_value = ?
                ,max_bid = ?
                ,is_house_sold = ?
                ,is_canceled = ?
                ,amount_sold = ?
                ,sold_to = ?
                ,is_watching = ?
                WHERE date = ? and case_number = ?""",
                house["Auction_Status"]
                ,house["Auction_type"]
                ,house["Judgement"]
                ,house["parcel_id"]
                ,house["address"]
                ,house["assessed_value"]
                ,house["max_bid"]
                ,house["is_house_sold"]
                ,house["is_canceled"] 
                ,house["amount_sold"]
                ,house["sold_to"] 
                ,house["is_watching"]
                ,house["date"]
                ,house["Case"])





def excel_report(data,path):
    
    workbook = xlsxwriter.Workbook(path + 'auction_audit2.xlsx') 
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
    print("writing to disk...")
    for line in data:
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

data = download_information()
save(data)
