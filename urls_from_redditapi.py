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
import mysql.connector
from mysql.connector import Error
# from manage_database import create_database_if_not_exists, connect_to_db, create_tables, save_data_to_db, save_comments_to_db,post_exists_in_db  # Import your database functions
from manage_database import *

# Access the environment variables
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

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