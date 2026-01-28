# Project Setup Guide

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/EthanYu888/Semester-2-Project.git
cd Semester-2-Project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Reddit API Credentials

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **Name**: WSB Sentiment Analyzer (or any name)
   - **App type**: Select "script"
   - **Description**: (optional)
   - **About URL**: (optional)
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Copy your credentials:
   - **Client ID**: The string under "personal use script"
   - **Client Secret**: The string next to "secret"

6. Create your `.env` file:
```bash
cp config/.env.example config/.env
```

7. Edit `config/.env` and add your credentials:
```bash
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_client_secret
REDDIT_USER_AGENT=WSB_Sentiment_Analyzer/1.0
```

### 5. Create Required Directories

The following directories should already exist (with .gitkeep files), but verify:

```bash
mkdir -p data/raw data/processed models logs
```

### 6. Test Your Setup

Create a simple test script to verify Reddit API access:

```python
import praw
from dotenv import load_dotenv
import os

load_dotenv('config/.env')

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Test connection
subreddit = reddit.subreddit('wallstreetbets')
print(f"Connected to r/{subreddit.display_name}")
print(f"Subscribers: {subreddit.subscribers:,}")

# Fetch one post to verify
for post in subreddit.hot(limit=1):
    print(f"\nSample post: {post.title}")
```

---

## Project Structure

```
Semester-2-Project/
├── config/
│   ├── .env.example          # Template for API credentials
│   └── config.yaml           # Project configuration
├── data/
│   ├── raw/                  # Raw scraped data (git-ignored)
│   └── processed/            # Cleaned/processed data (git-ignored)
├── docs/
│   ├── initial_stock_universe.md    # Stock selection documentation
│   ├── sentiment_analysis_approaches.md  # Sentiment methods research
│   └── setup_guide.md        # This file
├── models/                   # Trained models (git-ignored)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_sentiment_analysis.ipynb
├── src/
│   ├── data_collection/      # Reddit scraping scripts
│   ├── sentiment_analysis/   # Sentiment analysis modules
│   ├── modeling/             # ML model training
│   └── utils/                # Helper functions
├── logs/                     # Application logs (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Next Steps (Week 1-2)

- [x] Set up repository structure
- [x] Define initial stock universe (GME, AMC, TSLA, NVDA, SPY)
- [x] Research sentiment analysis approaches
- [ ] Set up Reddit API credentials
- [ ] Write data collection script for WSB posts
- [ ] Download historical stock price data (yfinance)
- [ ] Implement baseline VADER sentiment analysis
- [ ] Create initial data exploration notebook

---

## Development Workflow

### Daily Development

1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Pull latest changes:
   ```bash
   git pull origin main
   ```

3. Make your changes and test

4. Commit and push:
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   git push origin main
   ```

### Running Jupyter Notebooks

```bash
jupyter notebook
# Navigate to notebooks/ directory in the browser
```

### Running Scripts

```bash
# Example: Run data collection
python src/data_collection/scrape_wsb.py

# Example: Run sentiment analysis
python src/sentiment_analysis/analyze_sentiment.py
```

---

## Troubleshooting

### Reddit API Issues

**Problem**: "invalid_grant" or authentication errors

**Solution**: 
- Verify credentials in `.env` are correct
- Ensure no extra spaces in `.env` file
- Check that user agent is descriptive

**Problem**: Rate limiting (429 errors)

**Solution**:
- Add delays between requests (use `time.sleep()`)
- Respect Reddit's rate limits (60 requests per minute)

### Python Package Issues

**Problem**: Import errors for packages

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

**Problem**: PyTorch/Transformers installation issues

**Solution**:
- On Mac/Linux: Usually works with pip
- On Windows: May need to install PyTorch first separately
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install transformers
  ```

---

## Resources

- [PRAW Documentation](https://praw.readthedocs.io/)
- [Reddit API Rules](https://www.reddit.com/wiki/api/)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
- [FinBERT](https://huggingface.co/ProsusAI/finbert)
- [yfinance Documentation](https://pypi.org/project/yfinance/)

---

## Contact & Questions

For project-related questions, refer to:
- [README.md](../README.md) for project overview
- [docs/sentiment_analysis_approaches.md](sentiment_analysis_approaches.md) for technical details
- Create GitHub issues for bugs or feature requests
