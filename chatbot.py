import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from family_advisor import generate_family_advice_summary, build_llm_prompt
from llm_groq import call_groq_llm
import json

from nlp_helper import extract_intent_entities
from dsa_algos import (
    add_expense,
    total_expenses_by_category,
    highest_expense_category,
    lowest_expense_category,
    suggest_savings_plan,
    build_prefix_sum,
    monthly_expense_summary,
)
from visualizer import show_pie_chart, show_bar_chart
from emi_calculator import calculate_emi, savings_goal_plan

# -------------------- Data Utilities --------------------

def load_data():
    default_data = {
        "expenses": {
            "food": [],
            "transport": [],
            "entertainment": [],
            "utilities": [],
            "shopping": [],
        },
        "income": 0,
        "savings": 0,
        "logs": [],
        "family_profile": {
            "married": False,
            "spouse_income": 0,
            "children": [],
            "dependents": [],
        },
    }

    if not os.path.exists("finance_data.json"):
        with open("finance_data.json", "w") as f:
            json.dump(default_data, f)

    with open("finance_data.json", "r") as f:
        data = json.load(f)

    # Ensure all keys exist
    for key in default_data:
        if key not in data:
            data[key] = default_data[key]

    return data

def save_data(data):
    with open("finance_data.json", "w") as f:
        json.dump(data, f, indent=4)

# -------------------- App UI --------------------

st.set_page_config(page_title="💬 Financial Chatbot", layout="centered")
st.title("💬 Smart Financial Chatbot")
st.caption("Your personal finance assistant")

data = load_data()
expenses = data["expenses"]
income = data["income"]
savings = data["savings"]
logs = data.get("logs", [])
family = data.get("family_profile", {})

# -------------------- Chat Input --------------------

user_input = st.text_input("👤 You:", placeholder="e.g., Add expense of 300 for food")

if user_input:
    intent, entities = extract_intent_entities(user_input)

    if intent == "add_expense":
        if "amount" in entities and "category" in entities:
            data = add_expense(data, entities["category"], entities["amount"])
            data["logs"].append({
                "amount": entities["amount"], 
                "category": entities["category"], 
                "date": str(datetime.now().date())
            })
            save_data(data)
            st.success(f"✅ Added ₹{entities['amount']} to {entities['category']}")
        else:
            st.warning("⚠️ Please say like: Add expense of 500 for food")

    elif intent == "category_query":
        cat = entities.get("category")
        if cat and cat in expenses:
            total = sum(expenses[cat])
            st.info(f"💸 You've spent ₹{total} on {cat}")
        else:
            st.warning("⚠️ Couldn't find data for that category.")

    elif intent == "spending_analysis":
        totals = total_expenses_by_category(expenses)
        st.subheader("📊 Category-wise Spending")
        st.json(totals)
        st.info(highest_expense_category(expenses))
        st.info(lowest_expense_category(expenses))

    elif intent == "savings_check":
        total_expense = sum(sum(v) for v in expenses.values())
        st.info(f"💰 Income: ₹{income} | Expenses: ₹{total_expense} | Savings: ₹{savings}")
        st.success(suggest_savings_plan(income, total_expense))

    elif intent == "suggestion":
        st.info(highest_expense_category(expenses))
        st.success(suggest_savings_plan(income, sum(sum(v) for v in expenses.values())))

    else:
        st.warning("🤖 Sorry, I didn't understand that.")

# -------------------- Extra Tools --------------------

st.divider()
st.subheader("🧰 Tools & Utilities")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Show Pie Chart"):
        show_pie_chart(expenses)

with col2:
    if st.button("📊 Show Bar Chart"):
        show_bar_chart(expenses)

with st.expander("📅 Monthly Expense Summary"):
    if logs:
        df = pd.DataFrame(logs)
        df["amount"] = df["amount"].astype(float)
        df["date"] = pd.to_datetime(df["date"])
        prefix_df = build_prefix_sum(df)
        monthly_summary = monthly_expense_summary(prefix_df)
        st.bar_chart(monthly_summary)
    else:
        st.info("ℹ️ No expense logs available.")

with st.expander("💰 EMI Calculator"):
    p = st.number_input("Loan Amount (₹)", min_value=1000)
    r = st.number_input("Interest Rate (%)", min_value=1.0)
    t = st.number_input("Loan Duration (Months)", min_value=1)
    if st.button("Calculate EMI"):
        emi = calculate_emi(p, r, t)
        st.success(f"📈 Your EMI is ₹{emi}")

with st.expander("🎯 Goal Planner"):
    goal = st.number_input("Target Goal (₹)", min_value=1000)
    curr = st.number_input("Current Savings (₹)", min_value=0)
    months = st.number_input("Months to Achieve Goal", min_value=1)
    if st.button("Calculate Monthly Saving"):
        per_month = savings_goal_plan(goal, curr, months)
        st.success(f"🚀 You should save ₹{per_month} per month to reach your goal.")

# -------------------- Manual Data Setup --------------------

with st.expander("🛠️ Setup Income & Savings"):
    income = st.number_input("Monthly Income (₹)", value=income)
    savings = st.number_input("Current Savings (₹)", value=savings)
    if st.button("Save"):
        data["income"] = income
        data["savings"] = savings
        save_data(data)
        st.success("✅ Income & Savings updated!")

# -------------------- Family Profile --------------------

with st.expander("👪 Family Profile"):
    married = st.checkbox("Married?", value=family.get("married", False))
    spouse_income = st.number_input("Spouse Monthly Income (₹)", min_value=0, value=family.get("spouse_income", 0))

    # Children
    st.markdown("👶 Children Info")
    children_count = st.number_input("Number of Children", min_value=0, value=len(family.get("children", [])))
    children_ages = []
    for i in range(children_count):
        age = st.number_input(
            f"Age of Child {i + 1}", 
            min_value=0, 
            max_value=25,
            value=family.get("children", [])[i] if i < len(family.get("children", [])) else 0
        )
        children_ages.append(age)

    # Dependents
    st.markdown("👴 Other Dependents (like parents)")
    dependents = st.text_area("List of Dependents (comma-separated)", value=", ".join(family.get("dependents", [])))
    dependents_list = [dep.strip() for dep in dependents.split(",") if dep.strip()]

    if st.button("💾 Save Family Profile"):
        data["family_profile"] = {
            "married": married,
            "spouse_income": spouse_income,
            "children": children_ages,
            "dependents": dependents_list
        }
        save_data(data)
        st.success("✅ Family profile updated!")

# -------------------- Family Financial Advice --------------------

if st.button("📘 Generate Comprehensive Financial Plan"):
    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Rule-Based Recommendations")
        rule_based = generate_family_advice_summary(data)
        
        with st.expander("Budget Allocation"):
            st.json(rule_based["📊 Budget Advice"])
        
        with st.expander("Education Planning"):
            for tip in rule_based["🎓 Child Education"]:
                st.info(tip)
        
        with st.expander("Emergency Fund"):
            st.success(rule_based["💼 Emergency Fund"])
            
        if "👵 Spouse Retirement" in rule_based:
            with st.expander("Retirement Planning"):
                st.warning(rule_based["👵 Spouse Retirement"])
    
    with col2:
        st.subheader("🤖 AI-Powered Insights")
        with st.spinner("Generating personalized advice..."):
            prompt = build_llm_prompt(data)
            result = call_groq_llm(prompt)
            st.markdown(result)
        
        st.download_button(
            label="📥 Download Full Plan",
            data=json.dumps({
                "rule_based": rule_based,
                "ai_advice": result
            }, indent=4),
            file_name="family_financial_plan.json"
        )

# -------------------- GPT Advisor --------------------

with st.expander("🧠 Ask AI Suggestion"):
    if st.button("Get Groq LLM Suggestion"):
        from llm_groq import call_groq_llm
        prompt = f"""
        I'm a financial advisor. Here's my profile:
        - Monthly Income: ₹{income}
        - Spouse Income: ₹{family.get('spouse_income', 0)}
        - Savings: ₹{savings}
        - Number of Children: {len(family.get('children', []) )}
        - Expenses: {json.dumps(expenses)}

        Give personalized financial tips.
        """

        result = call_groq_llm(prompt)
        st.markdown(result)

# -------------------- End --------------------