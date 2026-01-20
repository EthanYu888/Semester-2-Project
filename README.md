# Semester-2-Project
I analyze whether online sentiment (e.g. WallStreetBets) has predictive power over short-term price movements.

Goal for semester 2 project: To test whether WallStreetBets sentiment and activity can predict short-term stock price movement

What I am predicting

A stock’s next-day direction:

Up (Green Day)
or
Down (Red Day)

Target Variable:
Next-day return direction

𝑦=1 if next-day return > 0, else 0

---

## Project Outline & Goals

### Primary Objective
This project aims to develop a machine learning model that leverages social media sentiment from WallStreetBets (WSB) to predict short-term stock price movements. The core question is: **Can online retail investor sentiment serve as a predictive signal for next-day stock returns?**

### Predictive Power
The model will provide:
- **Binary Classification**: Predict whether a stock will close up (green day) or down (red day) the following trading session
- **Sentiment Signal Strength**: Quantify the relationship between WSB discussion volume, sentiment scores, and actual price movements
- **Trading Insights**: Identify which sentiment metrics (upvotes, comment volume, positive/negative language) have the strongest predictive power
- **Risk Assessment**: Understand the reliability and limitations of social media sentiment as a trading indicator

### Success Metrics
- Classification accuracy > 55% (baseline: 50% random)
- Precision and recall for both up/down predictions
- Feature importance analysis showing significant sentiment variables
- Backtested strategy performance vs. buy-and-hold benchmark

---

## Bi-Weekly Timeline (January - April 2026)

### Week 1-2: Project Setup & Data Collection Planning (Jan 20 - Feb 2)
**Goals:**
- Set up Python environment with required libraries (PRAW, pandas, scikit-learn, yfinance)
- Create Reddit API credentials and test WSB data access
- Define initial stock universe (e.g., top 20 most-mentioned WSB stocks)
- Research and document relevant sentiment analysis approaches
- Set up GitHub repository structure with proper documentation

**Deliverables:**
- Working Reddit API connection
- List of target stocks to analyze
- Initial project structure and documentation

---

### Week 3-4: Data Collection & Storage (Feb 3 - Feb 16)
**Goals:**
- Scrape historical WSB posts and comments for selected stocks (ideally 6-12 months of data)
- Collect corresponding historical stock price data using yfinance
- Build data pipeline for ongoing data collection
- Store data in structured format (CSV/SQLite/Parquet)
- Perform initial data quality checks

**Deliverables:**
- Historical WSB dataset (posts, comments, timestamps, scores)
- Historical price dataset aligned with sentiment data
- Data collection scripts for automated updates
- Initial data quality report

---

### Week 5-6: Feature Engineering & Sentiment Analysis (Feb 17 - Mar 2)
**Goals:**
- Implement sentiment analysis (VADER, TextBlob, or FinBERT)
- Engineer features from WSB data:
  - Daily post/comment volume per stock
  - Aggregate sentiment scores
  - Upvote ratios and engagement metrics
  - Trending indicators (velocity of mentions)
- Create target variable (next-day return direction)
- Handle data alignment and time-zone issues
- Address missing data and outliers

**Deliverables:**
- Feature engineering pipeline
- Sentiment-labeled WSB dataset
- Combined dataset with features and target variable
- Exploratory data analysis (EDA) notebook

---

### Week 7-8: Exploratory Data Analysis & Baseline Model (Mar 3 - Mar 16)
**Goals:**
- Conduct comprehensive EDA:
  - Correlation between sentiment and returns
  - Distribution of features and target variable
  - Temporal patterns and trends
- Visualize key relationships
- Split data into train/validation/test sets (temporal split)
- Build baseline logistic regression model
- Establish performance benchmarks

**Deliverables:**
- EDA report with visualizations
- Train/validation/test datasets
- Baseline model with performance metrics
- Initial insights on feature-target relationships

---

### Week 9-10: Model Development & Experimentation (Mar 17 - Mar 30)
**Goals:**
- Experiment with multiple algorithms:
  - Random Forest
  - Gradient Boosting (XGBoost/LightGBM)
  - Neural Networks (if time permits)
- Perform hyperparameter tuning
- Implement cross-validation strategies
- Address class imbalance if present
- Feature selection and importance analysis

**Deliverables:**
- Multiple trained models with comparison metrics
- Hyperparameter tuning results
- Feature importance rankings
- Model selection justification

---

### Week 11-12: Model Evaluation & Refinement (Mar 31 - Apr 13)
**Goals:**
- Evaluate final model on test set
- Conduct detailed error analysis
- Test model robustness across different market conditions
- Implement backtesting framework for trading strategy
- Calculate risk-adjusted returns
- Identify model limitations and failure cases

**Deliverables:**
- Final model performance report
- Backtesting results with strategy metrics (Sharpe ratio, max drawdown)
- Error analysis and case studies
- Documented limitations and assumptions

---

### Week 13-14: Documentation & Final Presentation (Apr 14 - Apr 27)
**Goals:**
- Create comprehensive project documentation
- Develop final presentation/report with:
  - Problem statement and motivation
  - Methodology and approach
  - Results and key findings
  - Limitations and future work
- Clean and organize code repository
- Create visualizations for presentation
- Prepare demonstration/demo (if applicable)

**Deliverables:**
- Final project report (written)
- Presentation slides
- Clean, documented GitHub repository
- README with project overview and instructions
- Reflections on learnings and challenges

---

### Final Goal by End of April 2026

**Completed Machine Learning System** that:
1. Successfully predicts next-day stock price direction with statistically significant accuracy above baseline
2. Identifies which WallStreetBets sentiment metrics are most predictive of price movements
3. Demonstrates understanding of the relationship between social media sentiment and financial markets
4. Provides actionable insights on the viability of sentiment-based trading strategies
5. Includes comprehensive documentation of methodology, results, and limitations

**Key Deliverable**: A reproducible, well-documented project showcasing the full data science workflow from data collection through model deployment, with clear evidence of predictive power (or lack thereof) from WSB sentiment analysis.

---

## Notes & Considerations

- **Data Quality**: Reddit data can be noisy; plan for extensive cleaning
- **Market Events**: Consider excluding major market events (earnings, acquisitions) that could skew results
- **Survivorship Bias**: Be aware of stocks that were popular on WSB but no longer traded
- **Ethical Considerations**: This is for academic purposes; be cautious about real-world trading applications
- **Adaptability**: Timeline may need adjustments based on data availability and computational constraints
