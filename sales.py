# sales.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# --- Title ---
st.title("📊 Sales Dashboard")

# --- Load Sales Data Automatically from sales.csv ---
try:
    df = pd.read_csv("sales.csv")  # Make sure sales.csv is in the same folder
    st.subheader("📂 Data Preview")
    st.write(df.head())

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    if "Region" in df.columns:
        regions = st.sidebar.multiselect("Select Region(s)", df["Region"].unique(), default=df["Region"].unique())
        df = df[df["Region"].isin(regions)]

    if "Category" in df.columns:
        categories = st.sidebar.multiselect("Select Category(s)", df["Category"].unique(), default=df["Category"].unique())
        df = df[df["Category"].isin(categories)]

    # --- KPIs ---
    total_sales = df["Sales"].sum() if "Sales" in df.columns else 0
    total_profit = df["Profit"].sum() if "Profit" in df.columns else 0
    total_orders = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
    col3.metric("🛒 Total Orders", total_orders)

    # --- Charts ---
    st.subheader("📉 Sales by Category")
    if "Category" in df.columns and "Sales" in df.columns:
        category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales)

    st.subheader("🌍 Sales by Region")
    if "Region" in df.columns and "Sales" in df.columns:
        region_sales = df.groupby("Region")["Sales"].sum()
        fig, ax = plt.subplots()
        region_sales.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title("Sales Distribution by Region")
        st.pyplot(fig)

    st.subheader("📆 Sales Over Time")
    if "Order Date" in df.columns and "Sales" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        sales_time = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
        sales_time.index = sales_time.index.to_timestamp()

        st.line_chart(sales_time)

except FileNotFoundError:
    st.error("⚠️ sales.csv not found. Please make sure sales.csv is in the same folder as sales.py.")