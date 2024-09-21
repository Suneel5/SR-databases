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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()   

import praw

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

def post_exists(post_id, df):
    """Check if a post already exists in the DataFrame based on postid."""
    return post_id in df['postid'].values

def check_date_count(next_formatted_date, df):
    
    # Filter the DataFrame where the 'min_date' column matches the next_formatted_date
    count = df[df['min_date'] == next_formatted_date].shape[0]

    # Return True if the count is greater than 9, otherwise False
    return count > 9


# to use browser in background without displayingo on screen
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # User-agent spoofing

# Initialize the WebDriver 
# driver = webdriver.Chrome(options=chrome_options)
# Initialize the WebDriver 
driver = webdriver.Chrome()

df2=pd.read_csv('links_from_redditapi.csv')
def get_page_save_links(url,min_date,df):  

    # soup = BeautifulSoup(response.content, "html.parser")
    proxy=None
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http")) else None

    response=requests.get(url,
                        headers={
                "User-Agent": get_useragent()
            },
            proxies=None)
    
    # Open page
    driver.get(url)
    time.sleep(9)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    response=driver.page_source
            
    soup=BeautifulSoup(response,'html5lib')
    # soup=BeautifulSoup(response.text,'html5lib')
    result_block = soup.find_all("div", attrs={"class": "g"})

    results_no=0
    if not result_block:
        print(f"No results found for the URL: {url}")
        return df, 0
    for result in result_block:
        link = result.find("a", href=True)['href']
        postid=extract_postid(link)
        # Check if the post already exists in the CSV file
        if not post_exists(postid, df) and not post_exists(postid,df2):
            print(f'Link: {link}')
            # print(f'Postid: {postid}')
            dictt={'url': link, 
                'postid': postid,
                'min_date':min_date}
            new_row=pd.DataFrame([dictt])
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            print(f'Post: {postid} Already exists in csv file')

    # Save the updated DataFrame to the CSV file for every requests
    df.to_csv(csv_file, index=False)
    print(f"\nData has been written to {csv_file} successfully.\n")
    return df, len(result_block)

def format_date(date_obj):
    return date_obj.strftime('%m/%d/%Y')


end_date = datetime.strptime('2024-7-27', '%Y-%m-%d')
start_date = datetime.strptime('2024-06-29', '%Y-%m-%d')

# Iterate from start_date to end_date, one day at a time
current_date = end_date
i=0
while current_date >= start_date:
    # Convert the date to the required format (mm/dd/yyyy)
    formatted_date = format_date(current_date)
    # Move to the previous day
    prev_day = current_date - timedelta(days=2)
    next_formatted_date = format_date(prev_day)
    print(f'Min date: {next_formatted_date}      max date: {formatted_date}')
    # Construct the URL for the Google search

    start_page = 0
    no_of_output = 10
    url = f'https://www.google.com/search?q=realestateinvesting+reddit&tbs=cdr:1,cd_min:{next_formatted_date},cd_max:{formatted_date}&as_sitesearch=reddit.com/r/realestateinvesting/'
    # Pagination loop, continues until no_of_output < 10
    while no_of_output >= 10:
        # Construct the URL with pagination
        url = f'https://www.google.com/search?q=realestateinvesting+reddit&tbs=cdr:1,cd_min:{next_formatted_date},cd_max:{formatted_date}&as_sitesearch=reddit.com/r/realestateinvesting/&start={start_page}'
        
        # Call your function to scrape the page and save the links
        df, no_of_output = get_page_save_links(url, next_formatted_date, df)
        
        # If there are more than 9 results, move to the next page
        if no_of_output >= 10:
            print(f'Opening page {start_page // 10 + 2}')
            start_page += 10  # Increment for the next page
    # Add random delay between iterations (between 1 and 5 seconds)
    delay = random.uniform(1, 6)
    print(f'counter:{i}\n')
    print(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)  # Random sleep    
    
    # Move to the previous day
    current_date = prev_day
    
    if i>15:
        break
    i+=1

# driver.close()
