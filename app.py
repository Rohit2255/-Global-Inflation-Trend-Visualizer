import streamlit as st
import pandas as pd
import plotly.express as px

# Load your CPI data
df = pd.read_csv("cpi.csv")  # Change this filename accordingly

# Title and description
st.set_page_config(page_title="🌍 Global CPI Tracker", layout="centered")
st.title("🌍 Global CPI Tracker")
st.markdown("Explore the Consumer Price Index (CPI) trends of countries over the years.")

# Filter BRICS and G7 (optional)
brics = ["Brazil", "Russia", "India", "China", "South Africa"]
g7 = ["Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"]

# Sidebar Filters
st.sidebar.header("Select Options")
view_option = st.sidebar.radio("View Group", ["All Countries", "BRICS", "G7"])
if view_option == "BRICS":
    filtered_df = df[df["Country"].isin(brics)]
elif view_option == "G7":
    filtered_df = df[df["Country"].isin(g7)]
else:
    filtered_df = df.copy()
    

country = st.sidebar.selectbox("Choose a Country", sorted(filtered_df["Country"].unique()))
selected = filtered_df[filtered_df["Country"] == country]

# CPI Line Plot
fig = px.line(
    selected,
    x="Year",
    y="CPI",
    title=f"CPI Trend for {country} (1980s - 2022)",
    markers=True
)
fig.update_layout(yaxis_title="CPI", xaxis_title="Year")
st.plotly_chart(fig, use_container_width=True)

# Stats: Average CPI + Rank
latest_year_df = df[df["Year"] >= 2012]
avg_cpi_df = latest_year_df.groupby("Country")["CPI"].mean().reset_index()
avg_cpi_df["Rank"] = avg_cpi_df["CPI"].rank(ascending=False).astype(int)

country_stats = avg_cpi_df[avg_cpi_df["Country"] == country].iloc[0]
st.metric(label="📊 Avg CPI (2012–2022)", value=round(country_stats["CPI"], 2))
st.metric(label="🌍 Global Inflation Rank", value=int(country_stats["Rank"]))

