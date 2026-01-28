# Sentiment Analysis Approaches for WSB Data

## Overview

This document outlines relevant sentiment analysis methodologies for processing WallStreetBets text data to predict stock price movements.

---

## 1. Lexicon-Based Approaches

### VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Description**: Rule-based sentiment analysis specifically tuned for social media text.

**Advantages**:
- No training data required
- Handles emojis, slang, capitalization, and punctuation
- Fast and lightweight
- Provides compound, positive, negative, and neutral scores

**Disadvantages**:
- May miss WSB-specific jargon ("diamond hands", "stonks", "tendies")
- Cannot capture context-dependent sentiment

**Implementation**:
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores(text)
# Returns: {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.6}
```

**Best Use Case**: Baseline sentiment analysis, quick prototyping

---

### FinBERT (Financial BERT)

**Description**: Pre-trained BERT model fine-tuned on financial text for sentiment analysis.

**Advantages**:
- Understands financial context and terminology
- State-of-the-art performance on financial sentiment
- Classifies into positive, negative, neutral with confidence scores

**Disadvantages**:
- Slower than VADER (requires GPU for real-time processing)
- Trained on formal financial news, not WSB informal language
- Requires more computational resources

**Implementation**:
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
outputs = model(**inputs)
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
```

**Best Use Case**: Title and comment analysis, more accurate than VADER for financial content

---

### Custom WSB Lexicon

**Description**: Build a domain-specific sentiment dictionary with WSB terminology.

**Advantages**:
- Captures WSB-specific bullish/bearish language
- Can include emojis, slang, and community jargon
- Interpretable and customizable

**Disadvantages**:
- Requires manual curation
- Limited context understanding
- Needs regular updates as language evolves

**WSB-Specific Terms**:
- **Bullish**: 🚀 (rocket), 💎🙌 (diamond hands), HODL, moon, tendies, calls, long
- **Bearish**: 🌈🐻 (rainbow bear), puts, short, rug pull, bag holder
- **Neutral/Activity**: YOLO, ape, retard (self-deprecating), DD (due diligence)

**Implementation Approach**:
```python
wsb_lexicon = {
    'rocket': 2.0,  # Very bullish
    'moon': 2.0,
    'diamond hands': 1.5,
    'calls': 1.0,
    'puts': -1.0,
    'bag holder': -1.5,
    'rug pull': -2.0
}
```

**Best Use Case**: Supplement to VADER or as feature engineering for ML models

---

## 2. Machine Learning Approaches

### Supervised Classification (Logistic Regression, Random Forest, XGBoost)

**Description**: Train models on labeled WSB posts with known sentiment/price outcomes.

**Advantages**:
- Can learn WSB-specific patterns
- Feature engineering flexibility (n-grams, emoji counts, upvotes)
- Interpretable feature importance

**Disadvantages**:
- Requires labeled training data
- May overfit to specific time periods
- Feature engineering intensive

**Features to Extract**:
- TF-IDF vectors from post text
- Sentiment scores (VADER, FinBERT)
- Engagement metrics (upvotes, comments, awards)
- Post metadata (time, flair, author karma)
- Emoji counts and specific keyword presence

**Best Use Case**: When you have labeled data of WSB posts + next-day stock returns

---

### Deep Learning (LSTM, Transformer-based Models)

**Description**: Neural networks that can capture sequential patterns in text and time series.

**Advantages**:
- Can model temporal dependencies (e.g., sentiment trends over time)
- End-to-end learning from raw text
- State-of-the-art performance with sufficient data

**Disadvantages**:
- Requires large amounts of training data
- Black box models (less interpretable)
- Computationally expensive
- Risk of overfitting on small datasets

**Architecture Options**:
- **LSTM/GRU**: Process text sequences and time series jointly
- **BERT/RoBERTa**: Fine-tune on WSB posts with custom classification head
- **Multimodal**: Combine text embeddings with price/volume features

**Best Use Case**: Large-scale projects with extensive historical data (>10k posts)

---

## 3. Hybrid Approaches (RECOMMENDED)

### Multi-Signal Sentiment Aggregation

Combine multiple sentiment sources for robustness:

1. **VADER** for quick baseline sentiment
2. **FinBERT** for more accurate financial context
3. **Custom WSB lexicon** for community-specific signals
4. **Engagement metrics** as sentiment proxies (upvotes = community agreement)

**Aggregation Strategy**:
```python
# Weighted ensemble
final_sentiment = (
    0.3 * vader_compound +
    0.4 * finbert_positive_score +
    0.2 * wsb_lexicon_score +
    0.1 * normalized_upvote_ratio
)
```

**Advantages**:
- Reduces individual method weaknesses
- More robust across different post types
- Can weight based on empirical performance

---

## 4. Feature Engineering Beyond Sentiment

### Engagement Metrics
- **Upvote ratio**: Community agreement indicator
- **Comment count**: Discussion intensity
- **Awards**: Strong conviction signals (especially gold, platinum)
- **Posting velocity**: Sudden spikes in mentions

### Temporal Features
- **Time of day**: Market hours vs. after-hours posts
- **Day of week**: Weekend vs. weekday sentiment differences
- **Post age**: Decay function for older posts

### Author Credibility
- **Karma score**: Established vs. new users
- **Account age**: Filter out bots/spam
- **Historical accuracy**: Track users with good DD records (if feasible)

### Content Analysis
- **DD (Due Diligence) flair**: Higher signal quality
- **Meme flair**: Entertainment vs. actionable signal
- **Position screenshots**: Proof of conviction (calls/puts shown)

---

## 5. Recommended Implementation Path

### Phase 1: Baseline (Week 1-2)
1. Implement VADER for all posts
2. Extract basic engagement metrics
3. Aggregate daily sentiment scores per stock
4. Correlate with next-day returns

### Phase 2: Enhancement (Week 3-4)
1. Add FinBERT for post titles and top comments
2. Build custom WSB lexicon (top 50 terms)
3. Implement weighted ensemble scoring
4. Feature engineering (temporal, engagement)

### Phase 3: ML Integration (Week 5-8)
1. Create labeled dataset (post sentiment + next-day return)
2. Train supervised classifier (start with Logistic Regression)
3. Test Random Forest/XGBoost with all features
4. Compare ML performance vs. rule-based approaches

### Phase 4: Optimization (Week 9-12)
1. Hyperparameter tuning
2. Feature selection (identify most predictive signals)
3. Time-series validation (avoid lookahead bias)
4. Backtest trading strategy

---

## 6. Evaluation Metrics

### Sentiment Analysis Quality
- **Correlation**: Spearman correlation between sentiment and next-day returns
- **Classification Accuracy**: Predict up/down days from sentiment
- **ROC-AUC**: Discrimination power of sentiment scores

### Trading Performance
- **Precision/Recall**: For long (bullish) and short (bearish) signals
- **Sharpe Ratio**: Risk-adjusted returns from sentiment-based strategy
- **Max Drawdown**: Risk assessment

---

## 7. Key Challenges & Solutions

### Challenge 1: Sarcasm & Irony
WSB users are heavily sarcastic ("This stock is going to the moon... of bankruptcy")

**Solutions**:
- Context-aware models (BERT-based)
- Emoji analysis (🚀 vs. 💀)
- Engagement as truth signal (upvoted = genuine)

### Challenge 2: Pump & Dump Schemes
Coordinated manipulation to inflate sentiment

**Solutions**:
- Author credibility filtering
- Detect unusual spikes in mention volume
- Compare sentiment to fundamentals (volume, price action)

### Challenge 3: Lag & Timing
When to capture sentiment? Market close? Real-time?

**Solutions**:
- Multiple aggregation windows (4h, 12h, 24h before market open)
- Test different cutoff times (e.g., 9:00 AM ET)
- Account for after-hours trading

---

## 8. Tools & Libraries

### Python Libraries
```bash
pip install vaderSentiment transformers torch praw pandas numpy scikit-learn xgboost
```

### Key Packages
- **PRAW**: Reddit API wrapper for WSB data collection
- **vaderSentiment**: Quick lexicon-based sentiment
- **transformers**: Access to FinBERT and other pre-trained models
- **scikit-learn**: ML classifiers and evaluation
- **xgboost**: Gradient boosting for feature-rich models

---

## 9. Academic References

1. **Hutto & Gilbert (2014)**: "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text"
2. **Araci (2019)**: "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models"
3. **Cookson et al. (2023)**: "Social Media as a Bank Run Catalyst" (WSB & meme stocks)
4. **Umar et al. (2021)**: "The impact of COVID-19 on meme stock returns and market sentiment"

---

## 10. Implementation Checklist

- [ ] Install VADER and run on sample WSB posts
- [ ] Test FinBERT on financial vs. informal text
- [ ] Create initial WSB lexicon (20+ terms)
- [ ] Build post scraper with PRAW
- [ ] Aggregate daily sentiment per stock
- [ ] Visualize sentiment vs. price correlation
- [ ] Engineer engagement and temporal features
- [ ] Train baseline ML model (Logistic Regression)
- [ ] Evaluate with proper train/validation/test split
- [ ] Document findings and iterate

---

**Next Steps**: Proceed to data collection and begin with VADER + engagement metrics as baseline approach.
