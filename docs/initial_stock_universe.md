Week 1-2: Project Set Up

At the start of this project, I would like to first begin with choosing a few stocks that are most mentioned in wall street bets, just so that I would be able to get and gain plenty of useful information and data from those choices. 

# Initial Stock Universe

## Top 5 Most-Mentioned WallStreetBets Stocks (2025-2026)

Based on WSB historical trends and current market activity, the initial stock universe includes:

### 1. **GME (GameStop Corp.)**
- **Ticker**: GME
- **Sector**: Consumer Cyclical - Specialty Retail
- **Why WSB Favorite**: Original "meme stock" from 2021 short squeeze
- **Typical Characteristics**: High volatility, strong community following, frequent mention spikes

### 2. **AMC (AMC Entertainment Holdings)**
- **Ticker**: AMC
- **Sector**: Communication Services - Entertainment
- **Why WSB Favorite**: Second major short squeeze target, "ape" community
- **Typical Characteristics**: High retail ownership, social media-driven momentum

### 3. **TSLA (Tesla Inc.)**
- **Ticker**: TSLA
- **Sector**: Consumer Cyclical - Auto Manufacturers
- **Why WSB Favorite**: Cult following, Elon Musk factor, options activity
- **Typical Characteristics**: High liquidity, news-driven volatility, strong opinions

### 4. **NVDA (NVIDIA Corporation)**
- **Ticker**: NVDA
- **Sector**: Technology - Semiconductors
- **Why WSB Favorite**: AI boom leader, consistent gains, options-friendly
- **Typical Characteristics**: Strong fundamentals + meme appeal, high volume discussions

### 5. **SPY (SPDR S&P 500 ETF Trust)**
- **Ticker**: SPY
- **Sector**: Index ETF
- **Why WSB Favorite**: Most liquid options market, daily market direction plays
- **Typical Characteristics**: Benchmark for overall market sentiment, "0DTE" options popularity

## Selection Criteria

### Data Availability
- All stocks have:
  - High trading volume (>5M shares/day average)
  - Active options markets
  - Complete historical price data on Yahoo Finance
  - Frequent WSB discussion (multiple posts per week)

### Diversification
- Mix of individual stocks and ETF
- Multiple sectors represented
- Different volatility profiles
- Range of market capitalizations

### WSB Activity Metrics
Stocks selected based on:
- Mention frequency in daily discussion threads
- Number of dedicated posts per month
- Subreddit search volume
- Historical sentiment correlation with price movements

## Alternative/Backup Stocks

If data quality issues arise, consider these substitutes:
- **PLTR** (Palantir Technologies) - Tech/Defense
- **AAPL** (Apple Inc.) - Mega-cap tech
- **AMD** (Advanced Micro Devices) - Semiconductor alternative to NVDA
- **QQQ** (Invesco QQQ Trust) - Tech-heavy ETF alternative to SPY
- **BB** (BlackBerry Limited) - Historical WSB favorite

## Data Collection Notes

### Expected Characteristics
- **GME/AMC**: Episodic volatility, potential data gaps during low-activity periods
- **TSLA**: Consistent high-volume discussion, news confounding factors
- **NVDA**: Professional + retail interest, earnings-driven spikes
- **SPY**: Continuous discussion, macro sentiment indicator

### Potential Challenges
1. Stock splits or corporate actions affecting price continuity
2. Extended trading halts or delisting concerns (GME/AMC)
3. Distinguishing genuine sentiment from coordinated manipulation
4. Varying discussion quality between stocks

## Implementation Strategy

### Phase 1: Initial Testing
- Start with GME and SPY for model development
- GME: High sentiment impact, clear WSB signal
- SPY: Market baseline, high data volume

### Phase 2: Expansion
- Add TSLA and NVDA for tech sector coverage
- Add AMC for meme stock comparison

### Phase 3: Validation
- Compare results across all five stocks
- Identify which stock types benefit most from sentiment signals
- Refine universe based on predictive performance

## Data Collection Period

- **Historical Training Data**: 2 years (2024-2026)
- **Validation Period**: 3 months (Q1 2026)
- **Test Period**: Real-time/Future prediction

## References

- WSB mention frequency tools: Subreddit analytics sites, Reddit API
- Historical meme stock research: Academic papers on GME phenomenon
- Market data: Yahoo Finance, Alpha Vantage
