import matplotlib.pyplot as plt
import streamlit as st

def show_pie_chart(expenses):
    totals = {k: sum(v) for k, v in expenses.items()}
    categories = list(totals.keys())
    values = list(totals.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%')
    st.pyplot(fig)

def show_bar_chart(expenses):
    totals = {k: sum(v) for k, v in expenses.items()}
    fig, ax = plt.subplots()
    ax.bar(totals.keys(), totals.values(), color="skyblue")
    ax.set_ylabel("Amount ₹")
    ax.set_title("Spending by Category")
    st.pyplot(fig)
