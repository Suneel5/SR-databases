from datetime import datetime
# Record the start time
start_time = datetime.now()
print(f"Start Time: {start_time}")

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

import praw

# Access the environment variables
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
password = os.getenv('password')
user_agent = os.getenv('user_agent')
user_name = os.getenv('user_name')

# Authenticate using your Reddit API credentials
reddit = praw.Reddit(
    client_id=client_id,          
    client_secret=client_secret,  
#     password=password,
    user_agent=user_agent         
#     user_name=user_name
)
print()
print(reddit.user.me())
print()

def get_data_from_post(post_id):
        # Define the post ID 
        submission = reddit.submission(id=post_id)
        
        # Print post details
        
        title=submission.title if submission.title else ' '
        
        description=submission.selftext if submission.selftext else ' '
        tag=submission.link_flair_text if submission.link_flair_text else ' '

        print(f'Post ID: {post_id}')
        print(f"Title: {title}")
        # print(f"Description: {description}")
        print(f"Tag: {tag}")
        # Enable comment forest expansion to ensure nested comments are loaded
        submission.comments.replace_more(limit=None)
        comment_replies=[]
        # Iterate through the comments
        for top_level_comment in submission.comments:
                comment_replies.append(top_level_comment.body)
                # print(f"Comment: {top_level_comment.body}")
                for reply in top_level_comment.replies:
                        comment_replies.append(reply)
                        # print(f"Reply: {reply.body}")

        print('-' * 50)


#get post id from 
base_url='https://www.reddit.com/r/realestateinvesting/'

# to use browser in background without displayingo on screen
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # User-agent spoofing

# Initialize the WebDriver 
driver = webdriver.Chrome(options=chrome_options)

# Open page
driver.get(base_url)

# time.sleep(2)
#click on change post view
try:    
        try:
                change_view = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//shreddit-sort-dropdown[@header-text='View']"))
                        )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", change_view)
                ActionChains(driver).move_to_element(change_view).click().perform()
                print('change view clicked')
                time.sleep(3)

                #click on compact view
                compact_option = driver.find_element(By.XPATH, "//a[@href='?feedViewType=compactView']")
                ActionChains(driver).move_to_element(compact_option).click().perform()
                print('Compact view selected')
                time.sleep(3)
      
        except NoSuchElementException:
                print('change view button not found')
                pass  # No more "See more"
except Exception as e:
        print(f"Error while clicking 'change post view ': {e}") 


# time.sleep(2)
#scroll pages down 
pages=0
scraped_posts = set()
total_post=0
while pages<402:   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if pages%2==0:
                start_time2 = datetime.now()
                response=driver.page_source
                soup=BeautifulSoup(response,'html5lib')
                posts=soup.find_all('shreddit-post')
                new_posts=[post.get('id').replace('t3_', '') for post in posts]
                new=0
                for new_post in new_posts:
                        if new_post not in scraped_posts:
                                scraped_posts.add(new_post)
                                new+=1
                                get_data_from_post(new_post)
        # print(f"Total posts on page: {len(new_posts)} ")
        # print(f'\nTotal New Post :{new} on  scrolling {pages} times')

        end_time2 = datetime.now()
        elapsed_time = (end_time2 - start_time2).total_seconds() / 60
        print(f"\nscraped total {new} new post in {elapsed_time:.2f} minutes\n")
        print(f'Total post till now: {len(scraped_posts)}')
        print('#'*50)
        pages+=1
        
        
print(f'\nTotal unique post:{len(scraped_posts)}')

# Record the end time
end_time = datetime.now()
print(f"End Time: {end_time}")
# Calculate the elapsed time in minutes
elapsed_time = (end_time - start_time).total_seconds() / 60
print(f"Exceution Time: {elapsed_time:.2f} minutes")
