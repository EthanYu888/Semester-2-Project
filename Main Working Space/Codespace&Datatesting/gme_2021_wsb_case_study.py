#!/usr/bin/env python3
"""
GameStop 2021 short-squeeze case study.

This script shows how to evaluate whether WallStreetBets sentiment and activity
correlate with next-day GME price moves during 2021.

Usage:
  python src/modeling/gme_2021_wsb_case_study.py
  python src/modeling/gme_2021_wsb_case_study.py --wsb-csv data/raw/wsb_gme_posts.csv --no-plots

Expected WSB CSV columns (flexible):
- Required: date
- Optional text: title, body, text
- Optional engagement: score, num_comments
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import yfinance as yf
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler


@dataclass
class CaseStudyResult:
    merged_df: pd.DataFrame
    correlation_df: pd.DataFrame
    baseline_accuracy: float
    model_accuracy: float


def ensure_vader_lexicon() -> None:
    """Ensure NLTK VADER lexicon is available."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


def make_demo_gme_price_proxy() -> pd.DataFrame:
    """Build an illustrative 2021 GME-like price path for offline demos."""
    dates = pd.bdate_range("2021-01-04", "2021-12-31", freq="B")
    n = len(dates)

    # Smooth baseline path plus event spikes around Jan short squeeze.
    base = np.linspace(18, 28, n)
    noise = np.sin(np.linspace(0, 20, n)) * 1.4
    close = base + noise

    spike = (dates >= "2021-01-13") & (dates <= "2021-01-29")
    unwind = (dates >= "2021-02-01") & (dates <= "2021-02-12")
    close[spike] = close[spike] * np.linspace(2.2, 12.0, spike.sum())
    close[unwind] = close[unwind] * np.linspace(7.0, 2.0, unwind.sum())

    df = pd.DataFrame({"Date": dates})
    df["Close"] = np.clip(close, a_min=2, a_max=None)
    df["Open"] = df["Close"].shift(1).fillna(df["Close"].iloc[0]) * 0.995
    df["High"] = df[["Open", "Close"]].max(axis=1) * 1.03
    df["Low"] = df[["Open", "Close"]].min(axis=1) * 0.97
    df["Volume"] = 25_000_000
    df.loc[spike, "Volume"] = 120_000_000
    df.loc[unwind, "Volume"] = 90_000_000

    return df[["Date", "Open", "High", "Low", "Close", "Volume"]]


def load_gme_2021_prices() -> Tuple[pd.DataFrame, bool]:
    """Load GME daily prices for 2021, with network and offline fallbacks."""
    start = "2021-01-01"
    end = "2022-01-01"

    try:
        df = yf.download("GME", start=start, end=end, progress=False)
    except Exception:
        df = pd.DataFrame()

    if df is not None and not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        df = df.reset_index().sort_values("Date")
        cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
        return df[cols].copy(), False

    try:
        # Fallback: Stooq daily CSV
        stooq_url = "https://stooq.com/q/d/l/?s=gme.us&i=d"
        stooq = pd.read_csv(stooq_url)
        stooq["Date"] = pd.to_datetime(stooq["Date"])
        stooq = stooq[(stooq["Date"] >= start) & (stooq["Date"] < end)].copy()
        if not stooq.empty:
            stooq = stooq.sort_values("Date")
            cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
            return stooq[cols].reset_index(drop=True), False
    except Exception:
        pass

    return make_demo_gme_price_proxy(), True


def build_price_features(price_df: pd.DataFrame) -> pd.DataFrame:
    """Create return and target columns."""
    df = price_df.copy()
    df["Date"] = pd.to_datetime(df["Date"]).dt.floor("D")
    df["daily_return"] = df["Close"].pct_change()
    df["next_day_return"] = df["Close"].shift(-1) / df["Close"] - 1
    df["target_up_next_day"] = (df["next_day_return"] > 0).astype(int)
    return df.dropna().reset_index(drop=True)


def load_wsb_posts(wsb_csv: Path) -> pd.DataFrame:
    """Load WSB posts CSV, normalize columns, and combine text fields."""
    if not wsb_csv.exists():
        raise FileNotFoundError(f"WSB CSV not found: {wsb_csv}")

    df = pd.read_csv(wsb_csv)
    if df.empty:
        raise ValueError("WSB CSV exists but has no rows.")

    df.columns = [c.strip().lower() for c in df.columns]
    if "date" not in df.columns:
        raise ValueError("WSB CSV must include a 'date' column.")

    for col in ["title", "body", "text"]:
        if col not in df.columns:
            df[col] = ""

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.floor("D")
    df = df.dropna(subset=["date"]).copy()

    combined_text = (df["title"].fillna("") + " " + df["body"].fillna("") + " " + df["text"].fillna(""))
    df["combined_text"] = combined_text.str.strip()

    for col in ["score", "num_comments"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0

    return df


def make_demo_wsb_proxy(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an illustrative WSB activity/sentiment proxy around Jan 2021 squeeze dates.
    This is for demonstration only when real WSB post data is unavailable.
    """
    df = pd.DataFrame({"date": price_df["Date"].copy()})

    # In demo mode, build a signal that intentionally tracks future direction
    # so students can clearly see how the pipeline detects correlation.
    future_move = price_df["next_day_return"].shift(-1).fillna(0)
    move_sign = np.sign(future_move)
    strength = np.clip(np.abs(future_move) * 30, 0, 1)

    df["avg_sentiment"] = 0.1 + 0.7 * move_sign * (0.3 + 0.7 * strength)
    df["post_count"] = (40 + (120 * strength) + (20 * (move_sign > 0))).round().astype(int)
    df["sum_comments"] = (200 + (4500 * strength) + (500 * (move_sign > 0))).round().astype(int)
    df["sum_score"] = (300 + (7000 * strength) + (800 * (move_sign > 0))).round().astype(int)

    squeeze_window = (df["date"] >= "2021-01-13") & (df["date"] <= "2021-01-29")
    df.loc[squeeze_window, "avg_sentiment"] = 0.45
    df.loc[squeeze_window, "post_count"] = 450
    df.loc[squeeze_window, "sum_comments"] = 12000
    df.loc[squeeze_window, "sum_score"] = 22000

    unwind_window = (df["date"] >= "2021-02-01") & (df["date"] <= "2021-02-08")
    df.loc[unwind_window, "avg_sentiment"] = -0.20
    df.loc[unwind_window, "post_count"] = 220
    df.loc[unwind_window, "sum_comments"] = 5000
    df.loc[unwind_window, "sum_score"] = 6000

    return df


def aggregate_sentiment(posts_df: pd.DataFrame) -> pd.DataFrame:
    """Compute VADER compound sentiment and aggregate to daily features."""
    ensure_vader_lexicon()
    sia = SentimentIntensityAnalyzer()

    df = posts_df.copy()

    def score_text(text: str) -> float:
        text = text if isinstance(text, str) else ""
        if not text.strip():
            return 0.0
        return float(sia.polarity_scores(text)["compound"])

    df["compound"] = df["combined_text"].apply(score_text)

    daily = (
        df.groupby("date", as_index=False)
        .agg(
            avg_sentiment=("compound", "mean"),
            post_count=("combined_text", "count"),
            sum_comments=("num_comments", "sum"),
            sum_score=("score", "sum"),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )
    return daily


def merge_and_engineer(price_df: pd.DataFrame, wsb_daily: pd.DataFrame) -> pd.DataFrame:
    """Merge price + WSB daily features and build lagged predictors."""
    merged = price_df.merge(wsb_daily, left_on="Date", right_on="date", how="left")

    for col in ["avg_sentiment", "post_count", "sum_comments", "sum_score"]:
        if col not in merged.columns:
            merged[col] = 0.0
        merged[col] = merged[col].fillna(0)

    # Lag sentiment/activity by one trading day to avoid lookahead bias.
    for col in ["avg_sentiment", "post_count", "sum_comments", "sum_score"]:
        merged[f"{col}_lag1"] = merged[col].shift(1)

    merged = merged.dropna().reset_index(drop=True)
    return merged


def compute_correlations(merged_df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    """Compute Pearson and Spearman correlations against next-day return."""
    rows = []
    for col in feature_cols:
        pearson = merged_df[col].corr(merged_df["next_day_return"], method="pearson")
        spearman = merged_df[col].corr(merged_df["next_day_return"], method="spearman")
        rows.append({"feature": col, "pearson_r": pearson, "spearman_rho": spearman})

    out = pd.DataFrame(rows)
    out["abs_spearman"] = out["spearman_rho"].abs()
    out = out.sort_values("abs_spearman", ascending=False).drop(columns=["abs_spearman"])
    return out.reset_index(drop=True)


def evaluate_predictive_signal(merged_df: pd.DataFrame, feature_cols: List[str]) -> Tuple[float, float]:
    """Train a simple time-split logistic model and compare vs majority baseline."""
    X = merged_df[feature_cols].copy()
    y = merged_df["target_up_next_day"].astype(int).copy()

    split_idx = int(len(merged_df) * 0.7)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    majority = int(y_train.mode().iloc[0])
    baseline_pred = np.full(len(y_test), majority)
    baseline_acc = float(accuracy_score(y_test, baseline_pred))

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    model_acc = float(accuracy_score(y_test, pred))

    print("\nClassification Report (Logistic Regression):")
    print(classification_report(y_test, pred, digits=4, zero_division=0))

    return baseline_acc, model_acc


def print_case_summary(result: CaseStudyResult, used_proxy_data: bool, used_proxy_prices: bool) -> None:
    """Print a concise case-study interpretation."""
    print("\n" + "=" * 72)
    print("GME 2021 CASE STUDY SUMMARY")
    print("=" * 72)
    print(f"Rows analyzed: {len(result.merged_df)} trading days")
    print(f"Baseline accuracy: {result.baseline_accuracy:.4f}")
    print(f"WSB-feature model accuracy: {result.model_accuracy:.4f}")

    print("\nTop correlations with next-day return:")
    print(result.correlation_df.head(5).to_string(index=False))

    jan_window = result.merged_df[
        (result.merged_df["Date"] >= "2021-01-13") & (result.merged_df["Date"] <= "2021-01-29")
    ]
    if not jan_window.empty:
        print("\nShort-squeeze window sample (2021-01-13 to 2021-01-29):")
        sample_cols = ["Date", "Close", "daily_return", "avg_sentiment", "post_count", "sum_comments"]
        print(jan_window[sample_cols].head(10).to_string(index=False))

    if used_proxy_data:
        print("\nNOTE: This run used an illustrative WSB proxy, not real post-level WSB data.")
        print("To produce evidence-grade results, pass a real WSB CSV via --wsb-csv.")
    if used_proxy_prices:
        print("NOTE: This run also used an illustrative GME 2021 price proxy due data-source access issues.")

    if result.model_accuracy > result.baseline_accuracy:
        print("\nInterpretation: WSB sentiment/activity features added predictive signal over baseline.")
    else:
        print("\nInterpretation: WSB features did not clearly beat baseline in this run.")


def run_case_study(wsb_csv: Optional[Path], make_plots: bool) -> CaseStudyResult:
    """Run the full GME short-squeeze case study workflow."""
    prices, used_proxy_prices = load_gme_2021_prices()
    prices = build_price_features(prices)

    used_proxy_data = False
    if wsb_csv is not None and wsb_csv.exists():
        posts = load_wsb_posts(wsb_csv)
        wsb_daily = aggregate_sentiment(posts)
    else:
        used_proxy_data = True
        wsb_daily = make_demo_wsb_proxy(prices)

    merged = merge_and_engineer(prices, wsb_daily)

    feature_cols = [
        "avg_sentiment_lag1",
        "post_count_lag1",
        "sum_comments_lag1",
        "sum_score_lag1",
    ]

    corr_df = compute_correlations(merged, feature_cols)
    baseline_acc, model_acc = evaluate_predictive_signal(merged, feature_cols)

    if make_plots:
        plot_case_study(merged)

    result = CaseStudyResult(
        merged_df=merged,
        correlation_df=corr_df,
        baseline_accuracy=baseline_acc,
        model_accuracy=model_acc,
    )
    print_case_summary(result, used_proxy_data=used_proxy_data, used_proxy_prices=used_proxy_prices)
    return result


def plot_case_study(merged_df: pd.DataFrame) -> None:
    """Create compact visuals for price and WSB signal."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(merged_df["Date"], merged_df["Close"], label="GME Close")
    axes[0].set_title("GameStop (GME) Close Price - 2021")
    axes[0].set_ylabel("Price (USD)")
    axes[0].legend()

    axes[1].plot(merged_df["Date"], merged_df["avg_sentiment"], label="Avg WSB Sentiment", color="tab:orange")
    axes[1].plot(merged_df["Date"], merged_df["post_count"] / max(1, merged_df["post_count"].max()),
                 label="Normalized Post Count", color="tab:green")
    axes[1].set_title("WSB Sentiment and Activity")
    axes[1].set_ylabel("Signal")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GME 2021 short-squeeze WSB correlation case study")
    parser.add_argument(
        "--wsb-csv",
        type=Path,
        default=Path("data/raw/wsb_gme_posts.csv"),
        help="Path to WSB posts CSV. If missing, an illustrative proxy is used.",
    )
    parser.add_argument("--no-plots", action="store_true", help="Disable matplotlib charts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_case_study(wsb_csv=args.wsb_csv, make_plots=not args.no_plots)


if __name__ == "__main__":
    main()
