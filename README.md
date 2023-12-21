<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>Reddit Scraper</h1>

  <p>This Python script is designed to scrape data from a specified subreddit using the Reddit API, utilizing the PRAW library for interaction. The scraped data includes information about submissions and associated comments, and it is saved to a CSV file for further analysis.</p>

  <h2>Overview</h2>

  <p>The Reddit Scraper consists of several functions:</p>

  <ul>
    <li><strong>initialize_reddit:</strong> Initializes a connection to the Reddit API using provided credentials from the config file.</li>
    <li><strong>scrape_subreddit_data:</strong> Gathers data from the specified subreddit, including submission titles, authors, URLs, descriptions, post datetimes, and associated comments.</li>
    <li><strong>save_to_csv_chunk:</strong> Saves the collected data to a CSV file in chunks, allowing for incremental data storage.</li>
    <li><strong>scrape_and_save_subreddit:</strong> Combines the scraping and saving processes, making it easy to gather and store data from a subreddit in one step.</li>
  </ul>

  <h2>Usage</h2>

  <ol>
    <li><strong>Clone the Repository:</strong></li>
  </ol>

  <pre><code>git clone git@github.com:SaminRazeghi/Subreddit_Data.git
cd Subreddit_Data</code></pre>

  <ol start="2">
    <li><strong>Configure Reddit API Credentials:</strong></li>
  </ol>

  <p>Create a file named <code>config.py</code> with your Reddit API credentials:</p>

  <pre><code>
# config.py

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
USER_AGENT = "your_user_agent"
  </code></pre>

  <ol start="3">
    <li><strong>Install Dependencies:</strong></li>
  </ol>

  <p>Install the required Python packages:</p>

  <pre><code>pip install praw pandas</code></pre>

  <ol start="4">
    <li><strong>Run the Script:</strong></li>
  </ol>

  <p>Execute the script, specifying the desired subreddit to scrape:</p>

  <pre><code>python your_script.py
