import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="ApexPlanet | Sales Intelligence", page_icon="📊", layout="wide")
st.title("📊 Sales Intelligence Dashboard")
st.caption("ApexPlanet Data Analytics Internship — Task 3 | Deep-Dive: Customer Segmentation")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cleaned_sales_dataset.csv"
df = pd.read_csv(DATA_PATH)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce").fillna(0)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# KPI definitions use distinct Order_ID to avoid counting repeated order rows as separate orders.
customer = (df.groupby("Customer_ID", dropna=False)
    .agg(Total_Sales=("Total_Sales", "sum"),
         Order_Count=("Order_ID", "nunique"),
         Units=("Quantity", "sum"),
         Last_Order=("Order_Date", "max"))
    .reset_index())
snapshot_date = df["Order_Date"].max()
customer["Recency_Days"] = (snapshot_date - customer["Last_Order"]).dt.days
q75 = customer["Total_Sales"].quantile(.75)
customer["Segment"] = "Standard"
customer.loc[customer["Order_Count"] > 1, "Segment"] = "Repeat Customer"
customer.loc[customer["Total_Sales"] >= q75, "Segment"] = "High-Value Customer"
customer.loc[(customer["Order_Count"] > 1) & (customer["Total_Sales"] < q75), "Segment"] = "Repeat Customer"

st.sidebar.header("Dashboard Filters")
date_min, date_max = df["Order_Date"].min().date(), df["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
cities = sorted(df["City"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
genders = sorted(df["Gender"].dropna().unique().tolist())
sel_cities = st.sidebar.multiselect("City", cities, default=cities)
sel_categories = st.sidebar.multiselect("Category", categories, default=categories)
sel_genders = st.sidebar.multiselect("Gender", genders, default=genders)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
else:
    start_date, end_date = pd.Timestamp(date_min), pd.Timestamp(date_max) + pd.Timedelta(days=1)

f = df[(df["Order_Date"] >= start_date) & (df["Order_Date"] <= end_date)]
f = f[f["City"].isin(sel_cities) & f["Category"].isin(sel_categories) & f["Gender"].isin(sel_genders)]
orders = f["Order_ID"].nunique()
revenue = f["Total_Sales"].sum()
aov = revenue / orders if orders else 0
customers = f["Customer_ID"].nunique()
units = f["Quantity"].sum()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Average Order Value", f"₹{aov:,.0f}")
c4.metric("Unique Customers", f"{customers:,}")
c5.metric("Units Sold", f"{units:,.0f}")

st.divider()
left, right = st.columns(2)
with left:
    monthly = f.assign(Month=f["Order_Date"].dt.to_period("M").astype(str)).groupby("Month", as_index=False)["Total_Sales"].sum()
    fig = px.line(monthly, x="Month", y="Total_Sales", markers=True, title="Monthly Revenue Trend")
    st.plotly_chart(fig, use_container_width=True)
with right:
    cat = f.groupby("Category", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)
    fig = px.bar(cat, x="Category", y="Total_Sales", title="Revenue by Category", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Segmentation Deep-Dive")
st.caption("Segments are rule-based, calculated from each customer's full available history: High-Value = customer spend at or above the 75th percentile; Repeat = more than one distinct order and below the high-value threshold; Standard = all others.")
# Keep the segment definition stable for the dataset, then show selected customer segment counts.
seg = customer.groupby("Segment", as_index=False).agg(Customers=("Customer_ID","nunique"), Revenue=("Total_Sales","sum"))
l, r = st.columns(2)
with l:
    fig = px.pie(seg, names="Segment", values="Customers", hole=.45, title="Customers by Segment")
    st.plotly_chart(fig, use_container_width=True)
with r:
    fig = px.bar(seg, x="Segment", y="Revenue", title="Revenue by Customer Segment", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Value Explorer")
fc = customer.copy()
segment_options = ["All"] + sorted(fc["Segment"].unique().tolist())
chosen_segment = st.selectbox("Choose customer segment", segment_options)
if chosen_segment != "All":
    fc = fc[fc["Segment"] == chosen_segment]
fc = fc.sort_values("Total_Sales", ascending=False)
st.dataframe(fc.head(25).style.format({"Total_Sales":"₹{:,.2f}", "Recency_Days":"{:,.0f}"}), use_container_width=True)

st.subheader("City and Product Performance")
l, r = st.columns(2)
with l:
    city = f.groupby("City", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False).head(10)
    st.plotly_chart(px.bar(city, x="Total_Sales", y="City", orientation="h", title="Top 10 Cities by Revenue"), use_container_width=True)
with r:
    product = f.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False).head(10)
    st.plotly_chart(px.bar(product, x="Total_Sales", y="Product", orientation="h", title="Top 10 Products by Revenue"), use_container_width=True)

st.info("Data limitation: this dataset contains transaction-level sales records, not website visits or funnel events. It has limited repeat purchasing (many customers have one recorded order), so this dashboard uses transparent rule-based customer segments rather than claiming a robust retention or churn model.")
st.caption("Built with Python, Pandas, Streamlit and Plotly | ApexPlanet Task 3")
