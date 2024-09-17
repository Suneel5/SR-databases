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

def get_data_from_post(post_id,connection=None):
        # Define the post ID 
        submission = reddit.submission(id=post_id)
        
        # Print post details
        
        title=submission.title if submission.title else ' '
        
        description=submission.selftext if submission.selftext else ' '
        tag=submission.link_flair_text if submission.link_flair_text else ' '

        print(f'Post ID: {post_id}')
        print(f"Title: {title}")
        print(f"Tag: {tag}")
        print(f"Description: {description}")
        
        # Enable comment forest expansion to ensure nested comments are loaded
        submission.comments.replace_more(limit=None)
        comment_replies=[]
        # Iterate through the comments
        print('Comments: ')
        for top_level_comment in submission.comments:
                comment_replies.append(top_level_comment.body)
                # Retrieve the comment author
                comment_author = top_level_comment.author
                comment_author_name = comment_author.name if comment_author else "Unknown"
                print(f'{comment_author_name}: {top_level_comment.body}\n') 
                print("Replies: ")
                for reply in top_level_comment.replies:
                        # Retrieve the reply author
                        reply_author = reply.author
                        reply_author_name = reply_author.name if reply_author else "Unknown"
                        comment_replies.append(reply)
                        print(f"{reply_author_name}:{reply.body}")
        # comments_dump = '\n'.join(comment_replies)
        # save_data_to_db(connection, post_id, title, description, tag, comments_dump)

        print('-' * 50)