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
import re


#get post id from 
# base_url='https://www.reddit.com/r/realestateinvesting/'

# to use browser in background without displayingo on screen
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # User-agent spoofing

# Initialize the WebDriver 
driver = webdriver.Chrome(options=chrome_options)

def extract_postid(link):
    match=re.search(r'/comments/([a-zA-Z0-9]+)/', link)
    if match:
        return match.group(1)  # Returns only the post ID, like 18ygfte
    return None

# Initialize or load the CSV file if it exists
csv_file = 'link_from_tags.csv'
if os.path.exists(csv_file):
    # Load the existing CSV file
    df = pd.read_csv(csv_file)
else:
    # Create an empty DataFrame if the file doesn't exist
    df = pd.DataFrame(columns=['url','postid','min_date'])


def post_exists(post_id):
    """Check if a post already exists in the DataFrame based on postid."""
    return post_id in final_df['postid'].values


def url_from_tag(tag,df):
    url=f'https://www.reddit.com/r/RealEstate/?f=flair_name%3A"{tag}"'
    # Open page
    driver.get(url)

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
    pages=0
    scraped_posts = set()
    while pages<42:   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if pages%2==0:
                start_time2 = datetime.now()
                response=driver.page_source
                soup=BeautifulSoup(response,'html5lib')
                posts=soup.find_all('shreddit-post')
                new_posts=[post.get('id').replace('t3_', '') for post in posts]
                for new_post in new_posts:
                        #check if it is already in prev csv files
                        if new_post not in scraped_posts and not post_exists(new_post):
                                scraped_posts.add(new_post)
                                dictt={'url': 'from tag', 
                                'postid': new_post,
                                'min_date':'01/01/2000'}
                                new_row=pd.DataFrame([dictt])
                                df = pd.concat([df, new_row], ignore_index=True)
                                print('Post {new_post} Added')
                        
                        else:
                            print(f'Post: {new_post} Already exists in csv file')
                df.to_csv(csv_file, index=False)

                end_time2 = datetime.now()
                elapsed_time = (end_time2 - start_time2).total_seconds() / 60
                print(f'Total new till now in tag: {tag}: {len(scraped_posts)}')
        pages+=1
        
        
    print(f'\nTotal New post in Tag:{tag} ={len(scraped_posts)}')
    print('#'*50)
    return df


#combine links csv
df1=pd.read_csv('links.csv')
df2=pd.read_csv('links_from_redditapi.csv')

final_df= pd.concat([df1, df2], ignore_index=True)

#remove duplicates post id
final_df = final_df.drop_duplicates(subset='postid')

tags=['Rehabbing/Flipping', 'Commercial Real Estate', 'Legal', 'Self-Directed/Retirement Investing', 'Insurance', 'Wholesaling', 'Education', 'Foreclosure', 'Notes/Paper', 'Rent or Sell my House?', 'Property Management', '1031 Exchange', 'Multi-Family', '$20K Cabins', 'Land', 'Single Family Home', 'Vacation Rentals', 'Property Maintenance', 'Deal Structure', ' ', 'Humor', 'Foreign Investment', 'Construction', 'Finance', 'New Investor', 'Discussion', 'Self-Promotion - Monthly', 'Marketing', 'Software', 'Motivation - Monthly', 'Manufactured/Mobile Home', 'Taxes']
# tags_df=pd.read_csv('tags.csv')
# tags=tags_df['tag'].values
print(tags)
for tag in tags[2:]:
    if not tag==' ':
        print(f'\nTag: {tag}\n')
        df=url_from_tag(tag,df)



# Record the end time
end_time = datetime.now()
print(f"End Time: {end_time}")
# Calculate the elapsed time in minutes
elapsed_time = (end_time - start_time).total_seconds() / 60
print(f"Exceution Time: {elapsed_time:.2f} minutes")