"""
WSB Data Scraper

This script collects posts and comments from r/wallstreetbets for sentiment analysis.
"""

import praw
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
from tqdm import tqdm


def load_config():
    """Load Reddit API credentials from .env file"""
    load_dotenv('config/.env')
    
    return {
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'user_agent': os.getenv('REDDIT_USER_AGENT')
    }


def initialize_reddit_client(config):
    """Initialize PRAW Reddit client"""
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent=config['user_agent']
    )
    return reddit


def scrape_wsb_posts(reddit, stock_tickers, post_limit=100, lookback_days=7):
    """
    Scrape WSB posts mentioning specific stock tickers
    
    Args:
        reddit: PRAW Reddit instance
        stock_tickers: List of stock tickers to search for
        post_limit: Maximum posts to fetch per ticker
        lookback_days: How many days back to search
    
    Returns:
        pandas DataFrame with post data
    """
    subreddit = reddit.subreddit('wallstreetbets')
    posts_data = []
    
    cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
    
    print(f"Scraping r/wallstreetbets for tickers: {stock_tickers}")
    
    for ticker in tqdm(stock_tickers, desc="Processing tickers"):
        # Search for posts mentioning the ticker
        for post in subreddit.search(ticker, limit=post_limit, sort='new'):
            # Check if post is within lookback period
            post_date = datetime.utcfromtimestamp(post.created_utc)
            
            if post_date < cutoff_date:
                continue
            
            posts_data.append({
                'post_id': post.id,
                'ticker': ticker,
                'title': post.title,
                'selftext': post.selftext,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'created_utc': post_date,
                'author': str(post.author),
                'flair': post.link_flair_text,
                'url': post.url,
                'is_self': post.is_self
            })
            
            # Respect rate limits
            time.sleep(0.1)
    
    df = pd.DataFrame(posts_data)
    print(f"\nScraped {len(df)} posts")
    
    return df


def scrape_post_comments(reddit, post_ids, comment_limit=50):
    """
    Scrape top comments from specific posts
    
    Args:
        reddit: PRAW Reddit instance
        post_ids: List of post IDs to get comments from
        comment_limit: Max comments per post
    
    Returns:
        pandas DataFrame with comment data
    """
    comments_data = []
    
    print(f"Scraping comments from {len(post_ids)} posts")
    
    for post_id in tqdm(post_ids, desc="Processing posts"):
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # Don't expand "load more" comments
        
        for comment in submission.comments[:comment_limit]:
            comments_data.append({
                'comment_id': comment.id,
                'post_id': post_id,
                'body': comment.body,
                'score': comment.score,
                'created_utc': datetime.utcfromtimestamp(comment.created_utc),
                'author': str(comment.author)
            })
        
        time.sleep(0.1)
    
    df = pd.DataFrame(comments_data)
    print(f"Scraped {len(df)} comments")
    
    return df


def main():
    """Main execution function"""
    # Load configuration
    config = load_config()
    
    # Initialize Reddit client
    reddit = initialize_reddit_client(config)
    
    # Define stock universe
    stock_tickers = ['GME', 'AMC', 'TSLA', 'NVDA', 'SPY']
    
    # Scrape posts
    posts_df = scrape_wsb_posts(
        reddit, 
        stock_tickers, 
        post_limit=100, 
        lookback_days=7
    )
    
    # Save posts data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    posts_filename = f'data/raw/wsb_posts_{timestamp}.csv'
    posts_df.to_csv(posts_filename, index=False)
    print(f"\nPosts saved to: {posts_filename}")
    
    # Scrape comments from collected posts
    if len(posts_df) > 0:
        comments_df = scrape_post_comments(
            reddit, 
            posts_df['post_id'].tolist()[:50],  # Limit to first 50 posts for testing
            comment_limit=20
        )
        
        # Save comments data
        comments_filename = f'data/raw/wsb_comments_{timestamp}.csv'
        comments_df.to_csv(comments_filename, index=False)
        print(f"Comments saved to: {comments_filename}")
    
    print("\n✓ Data collection complete!")


if __name__ == "__main__":
    main()
