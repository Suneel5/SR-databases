# Subreddit Database

This project involves scraping posts from subreddits and creating a database to store post information, including titles, tags, descriptions, comments, and replies. The data is collected using various methods and stored in a structured database.

## Installation

To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

# Database Structure
The database consists of the following four tables: `title`, `comments`, `re_titles`, and `re_comments`. Below is a description of the entities in each table.

## Tables and Entities

### 1. `title`
| Column Name | Data Type | Description                         |
|-------------|------------|-------------------------------------|
| postno      | INT        | Unique post number                  |
| titleid     | VARCHAR    | Unique identifier for the title     |
| title       | TEXT       | Title of the post                   |
| tag         | VARCHAR    | Associated tag(s)                   |
| description | TEXT       | Content of the post                 |

### 2. `comments`
| Column Name  | Data Type | Description                                     |
|--------------|------------|-------------------------------------------------|
| commentid    | DATETIME   | Unique identifier for the comment               |
| titleid      | VARCHAR    | Foreign key referencing `title.titleid`         |
| userid       | VARCHAR    | ID Name of the user who commented               |
| comment      | TEXT       | Comment text                                    |

### 3. `re_titles`
| Column Name | Data Type | Description                         |
|-------------|------------|-------------------------------------|
| postno      | INT        | Unique post number                  |
| titleid     | VARCHAR    | Unique identifier for the title     |
| title       | VARCHAR    | Title of the reposted item          |
| tag         | VARCHAR    | Associated tag(s)                   |
| description | TEXT       | Description of the reposted item    |
| source      | VARCHAR    | Source of the reposted item         |

### 4. `re_comments`
| Column Name  | Data Type | Description                                     |
|--------------|------------|-------------------------------------------------|
| commented    | VARCHAR   | Unique identifier for the comment                |
| titleid      | VARCHAR   | Foreign key referencing `re_titles.titleid`      |
| userid       | VARCHAR   | ID of the user who commented on the repost       |
| comment      | TEXT      | Reposted comment text                            |

### Relationships
- The `comments` table references the `title` table via `titleid`.
- The `re_comments` table references the `re_titles` table via `titleid`.

## Adding New Posts to the Database
To add new posts from the subreddit into the existing database, follow these steps:

1. Open a terminal in the required folder (subreddit1 or subreddit2).

2. Run the following command:
 ```bash
python new_data_store.py
```
3. The new posts will be automatically added to the database



## Data Collection Methods

Posts are collected from different sources:

1. **Google Search Scraping (urls_from_gsearch)**  
   Extracts post links by scraping Google search pages, filtering results by date and site (Reddit).

2. **Reddit API Scraping (urls_from_redditapi)**  
   Scrapes new, top, rising, and hot posts from Reddit. This method can collect up to maax 2,000 unique posts only.

3. **Tag-based Scraping (urls_from_tags)**  
   Scrapes posts by filtering Reddit content based on tags.

All post links are saved in CSV format within the `posts_url` folder.


## Data Extraction and Storage
The script get_save_data.py is used to extract post information (title, tag, description, comments, replies) and save it to a database.








