import praw
import pandas as pd
from datetime import datetime
import time

def save_to_csv_chunk(df, csv_filename, chunk_size=100):
    try:
        existing_df = pd.read_csv(csv_filename)
        print(f"Loaded existing CSV file: {csv_filename}")
    except FileNotFoundError:
        existing_df = pd.DataFrame()
        print(f"CSV file not found, creating new file: {csv_filename}")

    combined_df = pd.concat([existing_df, df])
    combined_df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")

def wait_if_rate_limited(reddit):
    remaining_requests = reddit.auth.limits['remaining']
    if remaining_requests < 10:  # Adjust threshold if necessary
        sleep_time = reddit.auth.limits['reset_timestamp'] - time.time()
        print(f"Rate limit approaching, sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

user_agent = "Scraper by /u/samiiiiin"
reddit = praw.Reddit(
    client_id="ktfvEACaq0JNxg_159H3uw",
    client_secret="Q1NMWMsjIcWlaLBwEMl1r2vfr0w4ew",
    user_agent=user_agent,
)

# Create lists to store data
titles = []
url = []
authors = []
descriptions = []
datetimes = []
comments_data = []

chunk_size = 100
submission_counter = 0
total_submissions_fetched = 0

# Initialize `after` to None to start from the newest submission
after = None

print("Starting data collection from today, going back as far as possible...")

# Loop to handle pagination
while True:
    try:
        print(f"Fetching new submissions, starting after: {after}")
        submissions = reddit.subreddit('misophonia').new(limit=1000, params={'after': after})

        submission_fetched_this_batch = 0
        last_submission_id = None

        for submission in submissions:
            submission_time = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Processing submission: {submission.id}, created at {submission_time}")

            submission_counter += 1
            titles.append(submission.title)
            datetimes.append(datetime.utcfromtimestamp(submission.created_utc))
            authors.append(submission.author)
            url.append(submission.url)
            descriptions.append(submission.selftext)
            submission.comments.replace_more(limit=None)
            comments_data.append('\n'.join([f"Author: {comment.author}\nComment: {comment.body}" for comment in submission.comments.list()]))

            if len(titles) % chunk_size == 0:
                print(f"Reached {chunk_size} submissions, saving to CSV...")
                data = {
                    'Title': titles,
                    'Author': authors,
                    'Datetime': datetimes,
                    'URL': url,
                    'Description': descriptions,
                    'Comments': comments_data
                }

                df = pd.DataFrame(data)
                csv_filename = 'misophonia_data_from_today.csv'
                save_to_csv_chunk(df, csv_filename)
                titles.clear()
                authors.clear()
                datetimes.clear()
                url.clear()
                descriptions.clear()
                comments_data.clear()

            # Track the last submission's ID for pagination
            last_submission_id = submission.id
            submission_fetched_this_batch += 1

        # Stop if we've fetched all the relevant submissions
        if submission_fetched_this_batch == 0 or last_submission_id is None:
            print("No more submissions to fetch.")
            break

        # Update `after` with the last submission's ID to fetch the next batch
        after = last_submission_id
        print(f"Next batch will start after: {after}")

        total_submissions_fetched += submission_fetched_this_batch

        # Add a delay between requests to avoid hitting the rate limit
        print("Pausing for 2 seconds to avoid rate limits...")
        time.sleep(2)

        # Check the remaining rate limit
        wait_if_rate_limited(reddit)

    except praw.exceptions.APIException as e:
        if 'RATELIMIT' in str(e):
            print(f"Hit the rate limit, sleeping for 60 seconds... Error: {e}")
            time.sleep(60)  # Sleep for 60 seconds if rate limited
        else:
            print(f"APIException occurred: {e}")
            break

# Save any remaining data
if titles:
    print("Saving the remaining data to CSV...")
    data = {
        'Title': titles,
        'Author': authors,
        'Datetime': datetimes,
        'URL': url,
        'Description': descriptions,
        'Comments': comments_data
    }

    df = pd.DataFrame(data)
    save_to_csv_chunk(df, 'misophonia_data_from_today.csv')

# Log total numbers
print(f"Total submissions fetched in this run: {total_submissions_fetched}")
print(f"Total submissions processed: {submission_counter}")
