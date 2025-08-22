# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px

# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(
    page_title="Food Donation Dashboard",
    page_icon="🍱",
    layout="wide"
)

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    providers = pd.read_csv("providers_data.csv")
    receivers = pd.read_csv("receivers_data.csv")
    food_listings = pd.read_csv("food_listings_data.csv")
    claims = pd.read_csv("claims_data.csv")
    return providers, receivers, food_listings, claims

@st.cache_resource
def init_db(providers, receivers, food_listings, claims):
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    providers.to_sql("providers", conn, if_exists="replace", index=False)
    receivers.to_sql("receivers", conn, if_exists="replace", index=False)
    food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
    claims.to_sql("claims", conn, if_exists="replace", index=False)
    return conn

def run_query(conn, query, params=None):
    return pd.read_sql(query, conn, params=params)

# ------------------------------
# Data Load + DB Init
# ------------------------------
providers, receivers, food_listings, claims = load_data()
conn = init_db(providers, receivers, food_listings, claims)

# ------------------------------
# Dashboard Title
# ------------------------------
st.title("🍱 Food Donation Insights Dashboard")

# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.header("Filters")

cities = providers["City"].dropna().unique().tolist() if "City" in providers.columns else []
food_types = food_listings["Food_Type"].dropna().unique().tolist() if "Food_Type" in food_listings.columns else []

sel_city = st.sidebar.selectbox("City", ["All"] + sorted(map(str, cities))) if cities else "All"
sel_food = st.sidebar.selectbox("Food Type", ["All"] + sorted(map(str, food_types))) if food_types else "All"

# --- Build SQL filters dynamically ---
filters = []
params = {}

if sel_city != "All":
    filters.append("p.City = :city")
    params["city"] = sel_city
if sel_food != "All":
    filters.append("fl.Food_Type = :ft")
    params["ft"] = sel_food

filter_clause = " AND ".join(filters)
where_clause = f"WHERE {filter_clause}" if filters else ""

# ------------------------------
# KPI Metrics
# ------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Providers", len(providers))
col2.metric("Receivers", len(receivers))
col3.metric("Food Listings", len(food_listings))
col4.metric("Claims", len(claims))

# ------------------------------
# Monthly Claims Trend
# ------------------------------
st.subheader("📈 Monthly Claims Trend")
query = f"""
    SELECT strftime('%Y-%m', c.Timestamp) AS Month, COUNT(*) AS Total_Claims
    FROM claims c
    LEFT JOIN food_listings fl ON c.Food_ID = fl.Food_ID
    LEFT JOIN providers p ON fl.Provider_ID = p.Provider_ID
    {where_clause}
    GROUP BY Month
    ORDER BY Month;
"""
monthly = run_query(conn, query, params)
if not monthly.empty:
    fig = px.bar(monthly, x="Month", y="Total_Claims", title="Claims per Month")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No claims data available for the selected filters.")

# ------------------------------
# Top Providers
# ------------------------------
st.subheader("🏆 Top Providers by Donated Quantity")
query = f"""
    SELECT fl.Provider_ID, SUM(fl.Quantity) AS Total_Quantity
    FROM food_listings fl
    LEFT JOIN providers p ON fl.Provider_ID = p.Provider_ID
    {where_clause}
    GROUP BY fl.Provider_ID
    ORDER BY Total_Quantity DESC
    LIMIT 5;
"""
top_providers = run_query(conn, query, params)
st.dataframe(top_providers)

# ------------------------------
# Unclaimed Donations
# ------------------------------
st.subheader("🧾 Unclaimed Food Listings")
query = f"""
    SELECT fl.Food_ID, fl.Food_Name, fl.Food_Type, fl.Quantity, fl.Expiry_Date
    FROM food_listings fl
    LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
    LEFT JOIN providers p ON fl.Provider_ID = p.Provider_ID
    WHERE c.Claim_ID IS NULL
    {(" AND " + filter_clause if filters else "")}
    LIMIT 20;
"""
unclaimed = run_query(conn, query, params)
st.dataframe(unclaimed)

# ------------------------------
# Footer
# ------------------------------
st.caption("Developed with Streamlit | Food Donation Insights Dashboard")
