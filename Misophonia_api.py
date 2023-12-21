import praw
import pandas as pd
from praw.models import MoreComments
from datetime import datetime, timezone
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT

def initialize_reddit():
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )
    return reddit

def scrape_subreddit_data(subreddit_name, limit=None):
    reddit = initialize_reddit()

    # Create lists to store data
    titles = []
    url = []
    authors = []
    descriptions = []
    datetimes = []
    comments_data = []

    for submission in reddit.subreddit(subreddit_name).new(limit=limit):
        titles.append(submission.title)
        datetimes.append(datetime.utcfromtimestamp(submission.created_utc))
        authors.append(submission.author)
        url.append(submission.url)
        descriptions.append(submission.selftext)
        submission.comments.replace_more(limit=None)
        comments_data.append('\n'.join([f"Author: {comment.author}\nComment: {comment.body}" for comment in submission.comments.list()]))

    # Create a dictionary with the collected data
    data = {
        'Title': titles,
        'Author': authors,
        'Datetime': datetimes,
        'URL': url,
        'Description': descriptions,
        'Comments': comments_data
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    return df

def save_to_csv_chunk(df, csv_filename, chunk_size=100):
    # Check if the CSV file already exists
    try:
        existing_df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    # Concatenate the existing DataFrame with the new data
    combined_df = pd.concat([existing_df, df])

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(csv_filename, index=False)

    print(f'Data saved to {csv_filename}')

def scrape_and_save_subreddit(subreddit_name, csv_filename='reddit_data.csv', chunk_size=100, limit=None):
    df = scrape_subreddit_data(subreddit_name, limit)
    
    # Save the DataFrame to a CSV file in chunks
    save_to_csv_chunk(df, csv_filename, chunk_size)

# Example Usage:
scrape_and_save_subreddit('misophonia')
