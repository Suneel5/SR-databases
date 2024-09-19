from datetime import datetime
# Record the start time
start_time = datetime.now()
print(f"Start Time: {start_time}")

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import random
import re
from datetime import datetime, timedelta

load_dotenv()   

import praw
import mysql.connector
from mysql.connector import Error
# from manage_database import create_database_if_not_exists, connect_to_db, create_tables, save_data_to_db, save_comments_to_db,post_exists_in_db  # Import your database functions
from manage_database import *

# df=pd.read('')
def get_useragent():
    return random.choice(_useragent_list)

_useragent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]

def extract_postid(link):
    match=re.search(r'/comments/([a-zA-Z0-9]+)/', link)
    if match:
        return match.group(1)  # Returns only the post ID, like 18ygfte
    return None
    
# Initialize or load the CSV file if it exists
csv_file = 'links.csv'

if os.path.exists(csv_file):
    # Load the existing CSV file
    df = pd.read_csv(csv_file)
else:
    # Create an empty DataFrame if the file doesn't exist
    df = pd.DataFrame(columns=['url', 'postid','min_date'])

def get_page_save_links(url,min_date,df):  

    # soup = BeautifulSoup(response.content, "html.parser")
    proxy=None
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http")) else None

    response=requests.get(url,
                        headers={
                "User-Agent": get_useragent()
            },
            proxies=None)
            
    soup=BeautifulSoup(response.text,'html5lib')
    result_block = soup.find_all("div", attrs={"class": "g"})

    for result in result_block:
        link = result.find("a", href=True)['href']
        postid=extract_postid(link)
        print(f'Link: {link}')
        # print(f'Postid: {postid}')
        dictt={'url': link, 
               'postid': postid,
               'min_date':min_date}
        new_row=pd.DataFrame([dictt])
        df = pd.concat([df, new_row], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)
    print(f"\nData has been written to {csv_file} successfully.\n")
    return df

def format_date(date_obj):
    return date_obj.strftime('%m/%d/%Y')


end_date = datetime.strptime('2023-04-07', '%Y-%m-%d')
start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')

# Iterate from start_date to end_date, one day at a time
current_date = end_date
i=0
while current_date >= start_date:
    # Convert the date to the required format (mm/dd/yyyy)
    formatted_date = format_date(current_date)
    # Move to the previous day
    prev_day = current_date - timedelta(days=1)
    next_formatted_date = format_date(prev_day)
    print(f'Min date: {next_formatted_date}      max date: {formatted_date}')
    # Construct the URL for the Google search

    url = f'https://www.google.com/search?q=realestateinvesting+reddit&tbs=cdr:1,cd_min:{next_formatted_date},cd_max:{formatted_date}&as_sitesearch=reddit.com/r/realestateinvesting/'
    
    df=get_page_save_links(url,next_formatted_date,df)

    # Add random delay between iterations (between 1 and 5 seconds)
    delay = random.uniform(9, 17)
    print(f'counter:{i}\n')
    print(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)  # Random sleep    
    
    # Move to the previous day
    current_date = prev_day
    
    if i>80:
        break
    i+=1





    