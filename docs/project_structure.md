# Project Structure Documentation

## Directory Layout

```
Semester-2-Project/
│
├── config/                           # Configuration files
│   ├── .env.example                  # Template for API credentials
│   └── config.yaml                   # Project settings and parameters
│
├── data/                             # Data storage (git-ignored)
│   ├── raw/                          # Raw scraped data from Reddit and APIs
│   │   ├── wsb_posts_YYYYMMDD.csv
│   │   ├── wsb_comments_YYYYMMDD.csv
│   │   └── stock_prices_YYYYMMDD.csv
│   └── processed/                    # Cleaned and feature-engineered data
│       ├── merged_sentiment_prices.csv
│       └── training_data.csv
│
├── docs/                             # Project documentation
│   ├── initial_stock_universe.md     # Stock selection rationale
│   ├── sentiment_analysis_approaches.md  # Sentiment methods research
│   ├── setup_guide.md                # Installation and setup instructions
│   └── project_structure.md          # This file
│
├── models/                           # Trained ML models (git-ignored)
│   ├── baseline_logistic.pkl
│   ├── random_forest.pkl
│   └── model_performance.json
│
├── notebooks/                        # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb     # Initial EDA
│   ├── 02_sentiment_analysis.ipynb   # Sentiment testing
│   ├── 03_feature_engineering.ipynb  # Feature creation
│   └── 04_model_training.ipynb       # ML model experiments
│
├── src/                              # Source code modules
│   ├── data_collection/              # Data scraping scripts
│   │   ├── __init__.py
│   │   ├── scrape_wsb.py             # Reddit data collection
│   │   └── fetch_stock_prices.py     # Stock price download
│   │
│   ├── sentiment_analysis/           # Sentiment analysis modules
│   │   ├── __init__.py
│   │   ├── vader_analyzer.py         # VADER implementation
│   │   ├── finbert_analyzer.py       # FinBERT implementation
│   │   └── custom_lexicon.py         # WSB-specific lexicon
│   │
│   ├── modeling/                     # ML model training and evaluation
│   │   ├── __init__.py
│   │   ├── train_models.py           # Model training pipeline
│   │   ├── evaluate.py               # Model evaluation
│   │   └── predict.py                # Prediction script
│   │
│   └── utils/                        # Helper functions
│       ├── __init__.py
│       ├── data_preprocessing.py     # Data cleaning utilities
│       └── visualization.py          # Plotting functions
│
├── logs/                             # Application logs (git-ignored)
│   └── project.log
│
├── tests/                            # Unit tests (to be created)
│   ├── test_scraper.py
│   └── test_sentiment.py
│
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
└── README.md                         # Project overview
```

---

## Module Descriptions

### `/config`
Configuration files for the project. Keep sensitive data (API keys) in `.env` which is git-ignored.

**Key Files**:
- `.env`: Reddit API credentials (create from `.env.example`)
- `config.yaml`: Project parameters, stock tickers, model settings

---

### `/data`
All data files are stored here and excluded from version control via `.gitignore`.

**Subdirectories**:
- `raw/`: Unprocessed data directly from sources
- `processed/`: Cleaned, merged, and feature-engineered datasets ready for modeling

**Data Flow**:
1. Scrape WSB → `raw/wsb_posts.csv`
2. Fetch prices → `raw/stock_prices.csv`
3. Merge + engineer features → `processed/training_data.csv`

---

### `/docs`
Comprehensive project documentation for research, setup, and methodology.

**Contents**:
- Research on stock selection and sentiment methods
- Setup guides for reproducibility
- Architecture and design decisions

---

### `/models`
Trained machine learning models and performance metrics. Git-ignored to avoid large file commits.

**Typical Contents**:
- Serialized models (.pkl, .h5, .pt files)
- Model performance JSON files
- Hyperparameter tuning results

---

### `/notebooks`
Jupyter notebooks for interactive exploration, experimentation, and visualization.

**Workflow**:
1. `01_data_exploration.ipynb`: Understand raw data distributions
2. `02_sentiment_analysis.ipynb`: Test VADER, FinBERT on sample posts
3. `03_feature_engineering.ipynb`: Create and validate features
4. `04_model_training.ipynb`: Train and compare models

---

### `/src`
Core source code organized into logical modules.

#### `data_collection/`
Scripts to gather data from external sources.

**Files**:
- `scrape_wsb.py`: Collect Reddit posts and comments using PRAW
- `fetch_stock_prices.py`: Download historical stock data via yfinance

#### `sentiment_analysis/`
Sentiment analysis implementations.

**Files**:
- `vader_analyzer.py`: VADER sentiment scores
- `finbert_analyzer.py`: FinBERT transformer-based sentiment
- `custom_lexicon.py`: WSB-specific term scoring

#### `modeling/`
Machine learning pipeline for training and evaluation.

**Files**:
- `train_models.py`: Model training with cross-validation
- `evaluate.py`: Performance metrics (accuracy, precision, ROC-AUC)
- `predict.py`: Generate predictions on new data

#### `utils/`
Reusable helper functions.

**Files**:
- `data_preprocessing.py`: Cleaning, normalization, feature scaling
- `visualization.py`: Plotting functions for EDA and results

---

### `/logs`
Application logs for debugging and monitoring. Git-ignored.

---

### `/tests`
Unit tests to ensure code reliability (to be implemented).

---

## Data Pipeline Overview

```
┌─────────────────┐
│  Reddit API     │
│  (PRAW)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ scrape_wsb.py   │      │ fetch_stock_     │
│                 │      │ prices.py        │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         ▼                        ▼
    raw/wsb_posts.csv      raw/stock_prices.csv
         │                        │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │ Sentiment Analysis │
         │ + Feature Eng.     │
         └────────┬───────────┘
                  │
                  ▼
         processed/training_data.csv
                  │
                  ▼
         ┌────────────────────┐
         │ Model Training     │
         │ (train_models.py)  │
         └────────┬───────────┘
                  │
                  ▼
         models/trained_model.pkl
                  │
                  ▼
         ┌────────────────────┐
         │ Evaluation &       │
         │ Backtesting        │
         └────────────────────┘
```

---

## Version Control Best Practices

### What to Commit
- ✓ Source code (`src/`)
- ✓ Documentation (`docs/`)
- ✓ Configuration templates (`.env.example`, `config.yaml`)
- ✓ Requirements (`requirements.txt`)
- ✓ Notebooks (with outputs cleared)

### What NOT to Commit (in `.gitignore`)
- ✗ API credentials (`.env`)
- ✗ Raw/processed data (`data/`)
- ✗ Trained models (`models/`)
- ✗ Logs (`logs/`)
- ✗ Virtual environment (`venv/`)

---

## Running the Full Pipeline

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Collect WSB data
python src/data_collection/scrape_wsb.py

# 3. Fetch stock prices
python src/data_collection/fetch_stock_prices.py

# 4. Run sentiment analysis + feature engineering
python src/sentiment_analysis/vader_analyzer.py

# 5. Train models
python src/modeling/train_models.py

# 6. Evaluate performance
python src/modeling/evaluate.py
```

---

## Future Expansion Ideas

- Add `/scripts` folder for one-off utilities
- Create `/api` folder for Flask/FastAPI deployment
- Add `/dashboards` for Streamlit/Plotly Dash visualizations
- Implement CI/CD with GitHub Actions (`.github/workflows/`)

---

**Last Updated**: January 28, 2026
