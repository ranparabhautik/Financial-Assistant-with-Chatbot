from collections import defaultdict
import heapq
import pandas as pd
from datetime import datetime

def build_prefix_sum(expenses_with_date):
    df = pd.DataFrame(expenses_with_date)
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values(by="date", inplace=True)
    df["cumulative"] = df["amount"].cumsum()
    return df

def monthly_expense_summary(df):
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum().to_dict()

def add_expense(data, category, amount):
    if category not in data["expenses"]:
        data["expenses"][category] = []
    data["expenses"][category].append(amount)
    return data

def total_expenses_by_category(expenses):
    totals = {}
    for cat, values in expenses.items():
        totals[cat] = sum(values)
    return totals

def highest_expense_category(expenses):
    totals = total_expenses_by_category(expenses)
    if not totals:
        return "No expenses yet."
    max_cat = max(totals, key=totals.get)
    return f"Your highest spending is in '{max_cat}' category: ₹{totals[max_cat]}"

def lowest_expense_category(expenses):
    totals = total_expenses_by_category(expenses)
    if not totals:
        return "No expenses yet."
    min_cat = min(totals, key=totals.get)
    return f"Your lowest spending is in '{min_cat}' category: ₹{totals[min_cat]}"

def suggest_savings_plan(income, total_expense):
    # Greedy algorithm: Save as much as possible
    possible_saving = income - total_expense
    if possible_saving <= 0:
        return "You're overspending. Try cutting expenses."
    elif possible_saving < income * 0.2:
        return f"You are saving ₹{possible_saving}, but you could try saving more."
    else:
        return f"Great! You're saving ₹{possible_saving} which is a good habit."
