# time_analyzer.py

from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict

# Prepares a prefix sum-style structure per category
def build_category_prefix_logs(logs):
    df = pd.DataFrame(logs)
    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    return df

# Returns total expense for a category over N days
def expense_last_n_days(df, category, days):
    recent_date = df["date"].max()
    from_date = recent_date - timedelta(days=days)
    filtered = df[(df["category"] == category) & (df["date"] >= from_date)]
    return filtered["amount"].sum()

# Returns average monthly expense per category
def average_monthly_expense(df):
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby(["category", "month"])["amount"].sum().groupby("category").mean().to_dict()

# Returns category with max average spending in last N months
def highest_avg_spending_category(df, months):
    recent_date = df["date"].max()
    from_date = recent_date - pd.DateOffset(months=months)
    df = df[df["date"] >= from_date]
    avg = average_monthly_expense(df)
    if not avg:
        return "No data available."
    max_cat = max(avg, key=avg.get)
    return f"📈 Highest average spending category in last {months} months: {max_cat} (₹{avg[max_cat]:.2f})"
