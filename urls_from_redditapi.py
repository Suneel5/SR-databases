from datetime import datetime
import os
import praw
import pandas as pd
import time
import random
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Reddit API authentication
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Print the Reddit user
print(f"Authenticated as: {reddit.user.me()}\n")

# Initialize or load the CSV file if it exists
csv_file = 'posts_url/links_from_redditapi.csv'
if os.path.exists(csv_file):
    # Load the existing CSV file
    df = pd.read_csv(csv_file)
else:
    # Create an empty DataFrame if the file doesn't exist
    df = pd.DataFrame(columns=['url', 'postid', 'min_date'])

# Define the subreddit and categories
subreddit = reddit.subreddit('RealEstate')
categories = ['hot', 'top', 'new', 'rising']

def get_posts_from_category(category):
    """Fetch posts from a specific category."""
    if category == 'hot':
        return subreddit.hot(limit=1000)
    elif category == 'top':
        return subreddit.top(limit=1000)
    elif category == 'new':
        return subreddit.new(limit=1000)
    elif category == 'rising':
        return subreddit.rising(limit=1000)

def post_exists(post_id, df):
    """Check if a post already exists in the DataFrame based on postid."""
    return post_id in df['postid'].values

# Loop through each category and fetch posts
for category in categories:
    print(f"\nFetching posts from category: {category}")
    
    posts = get_posts_from_category(category)
    
    for post in posts:
        # Convert Unix timestamp to human-readable format
        date_posted = datetime.fromtimestamp(post.created_utc)
        post_id = post.id
        
        # Check if the post already exists in the CSV file
        if not post_exists(post_id, df):
            print(f"New Post - URL: {post.url}, Post ID: {post_id}, Date Posted: {date_posted}")
            
            # Create a dictionary for the new post
            new_post = {
                'url': post.url,
                'postid': post_id,
                'min_date': date_posted
            }
            
            # Add new post to the DataFrame
            new_row = pd.DataFrame([new_post])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save the updated DataFrame to the CSV file
            df.to_csv(csv_file, index=False)
            print(f"Post saved to {csv_file}.")
        else:
            print(f"Post {post_id} already exists in CSV.")

    # Add a random delay between category fetches to avoid rate limits
    delay = random.uniform(3, 7)
    print(f"\nWaiting {delay:.2f} seconds before fetching the next category...\n")
    time.sleep(delay)

print("\nAll categories processed.")
