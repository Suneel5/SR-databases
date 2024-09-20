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
tags=[]
def get_data_save(post_id,connection):
        # Define the post ID 
        submission = reddit.submission(id=post_id)
        
        # Print post details
        
        title=submission.title if submission.title else ' '
        
        description=submission.selftext if submission.selftext else ' '
        tag=submission.link_flair_text if submission.link_flair_text else ' '
        tags.append(tag)
        print(f'Post ID: {post_id}')
        # print(f"Title: {title}")
        print(f"Tag: {tag}")
        # print(f"Description: {description}")
        # Check if the post already exists in the database
        if not post_exists_in_db(connection, post_id):
                # If the post does not exist, insert the post details
                print('Writing data in db')
                save_data_to_db(connection, post_id, title, tag, description)

                # Enable comment forest expansion to ensure nested comments are loaded
                submission.comments.replace_more(limit=None)
                # Iterate through the comments
                # print('Comments: ')
                comments=[]
                for top_level_comment in submission.comments:
                        # Retrieve the comment author
                        comment_author = top_level_comment.author
                        comment_author_name = comment_author.name if comment_author else "Unknown"
                        # Add comment to the comments list
                        
                        save_comments_to_db(connection, post_id,comment_author_name, top_level_comment.body)
                        # print(f'{comment_author_name}: {top_level_comment.body}\n') 

                        # print("Replies: ")
                        for reply in top_level_comment.replies:
                                # Retrieve the reply author
                                reply_author = reply.author
                                reply_author_name = reply_author.name if reply_author else "Unknown"
                                # Add reply to the comments list
                                
                                save_comments_to_db(connection, post_id,reply_author_name, reply.body)
                                # print(f"{reply_author_name}:{reply.body}")
                # After gathering all comments and replies, insert them into the database
                print('-' * 50)


#combine links csv
df1=pd.read_csv('posts_url/links.csv')
df2=pd.read_csv('posts_url/links_from_redditapi.csv')

final_df= pd.concat([df1, df2], ignore_index=True)

#remove duplicates post id
final_df = final_df.drop_duplicates(subset='postid')
final_df.to_csv('posts_url/final_links.csv', index=False)
print(f"\nData has been written to 'final_links.csv' successfully.\n")


# Step 1: Database Initialization
create_database_if_not_exists()  # Create database if not exists
connection = connect_to_db()  # Connect to the database
create_tables(connection)  # Create tables if not exist


# call get data for all postid
# for postid in final_df['postid'].values[:4000]:
#     get_data_save(postid,connection)
#     time.sleep(2)


# Close the DB connection
if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")


tags=set(tags)
tags=list(tags)

print(tags)
# Convert the list to a DataFrame
df = pd.DataFrame(tags, columns=['tag'])

# Save the DataFrame to a CSV file (one element per row)
df.to_csv('tags.csv', index=False)

# Record the end time
end_time = datetime.now()
print(f"End Time: {end_time}")
# Calculate the elapsed time in minutes
elapsed_time = (end_time - start_time).total_seconds() / 60
print(f"Exceution Time: {elapsed_time:.2f} minutes")