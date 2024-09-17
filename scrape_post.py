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
load_dotenv()

base_url='https://www.reddit.com/r/realestateinvesting/'

import praw

# Authenticate using your Reddit API credentials
reddit = praw.Reddit(
    client_id='DL1gYnvsO1gYdQz4ptee2g',          
    client_secret='jK7BZRCQubEICyORXgu1N_BVnGF85w',  
    password='@Reddit2060',
    user_agent='Scrape post by  u/Fluid_Mark5687',         
    user_name='Fluid_Mark5687'
)
print()
print(reddit.user.me())
print()

# Define the post ID 
submission = reddit.submission(id="1fgmuyq")

# Print post details
print(f"Title: {submission.title}")
print(f"Description: {submission.selftext}")
print(f"Tag: {submission.link_flair_text}")
# Enable comment forest expansion to ensure nested comments are loaded
submission.comments.replace_more(limit=None)

# Iterate through the comments
print('\nCOmment and replies: ')
for top_level_comment in submission.comments:
    # print(f"Author: {top_level_comment.author}")
    print(f" {top_level_comment.body}")
    for reply in top_level_comment.replies:
        print(f" {reply.body}")
    print('-' * 50)


# Record the end time
end_time = datetime.now()
print(f"End Time: {end_time}")

# Calculate the elapsed time in minutes
elapsed_time = (end_time - start_time).total_seconds() / 60
print(f"Exceution Time: {elapsed_time:.2f} minutes")

