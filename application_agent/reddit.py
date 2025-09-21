# reddit_listener.py

import os
from dotenv import load_dotenv
import praw
from agents.agents import agent_handler

# --- 1. LOAD SECURE CREDENTIALS ---
load_dotenv()

# Load Reddit credentials from the .env file
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
USER_AGENT = "MyRedditListener v1.0 by u/" + str(USERNAME)

# The subreddit you want to monitor. Use '+' to monitor multiple, e.g., "learnpython+worldnews"
SUBREDDIT_TO_MONITOR = "AskReddit"

# --- 2. THE REDDIT CLIENT AND STREAM LISTENER ---
try:
    # Connect to Reddit using the credentials
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD,
    )
    
    # Access the specific subreddit
    subreddit = reddit.subreddit(SUBREDDIT_TO_MONITOR)
    
    print(f"✅ Script is running and listening for new posts in r/{subreddit.display_name}...")
    
    # This is the real-time "listener." It waits for new posts to appear.
    # skip_existing=True ensures you don't get a flood of old posts on startup.
    content = ""
    for submission in subreddit.stream.submissions(skip_existing=True):
        # --- THIS IS YOUR "NOTIFICATION" IN THE SERVER TERMINAL ---
        content += submission.selftext
        if len(content) >300:
            result = agent_handler(content)
            print("Misinformation checker results:", result)
            content = ""
        print("-----------------------------------------")
        print(f"🔥 NEW REDDIT POST FOUND")
        print(f"   - Subreddit: r/{submission.subreddit.display_name}")
        print(f"   - Author: u/{submission.author}")
        print(f"   - Title: \"{submission.title}\"")
        print(f"   - Link: {submission.shortlink}")
        print("-----------------------------------------")
        print()

except Exception as e:
    print(f"An error occurred: {e}")