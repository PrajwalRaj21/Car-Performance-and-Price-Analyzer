import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/Cleaned Dataset.csv")

df = load_data()

# -------------------------------------------
# Title & Description
# -------------------------------------------
st.set_page_config(page_title="Car Performance & Price in $ Analyzer", layout="wide")
st.title("🚗 Car Performance & Price in $ Analyzer")
st.markdown("""
Analyze car performance, Price in $s, and fuel efficiency.  
Filter by brand and budget, and explore cars visually.
""")

# -------------------------------------------
# Sidebar filters
# -------------------------------------------
st.sidebar.header("🔍 Filters")

make_filter = st.sidebar.multiselect(
    "Select Car Brand(s):",
    options=df["Make"].unique(),
    default=[]
)

budget = st.sidebar.slider(
    "Select Max Budget ($):",
    int(df["Price in $"].min()),
    int(df["Price in $"].max()),
    int(df["Price in $"].median())
)

filtered_df = df.copy()
if make_filter:
    filtered_df = filtered_df[filtered_df["Make"].isin(make_filter)]
filtered_df = filtered_df[filtered_df["Price in $"] <= budget]

# -------------------------------------------
# Dataset preview
# -------------------------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head())

# -------------------------------------------
# Cars per Brand
# -------------------------------------------
st.subheader("🏷️ Number of Cars per Brand")
brand_counts = filtered_df["Make"].value_counts().reset_index()
brand_counts.columns = ["Make", "Car Count"]

fig_brand = px.bar(
    brand_counts,
    x="Make",
    y="Car Count",
    title="Number of Cars per Brand",
    text_auto=True
)
st.plotly_chart(fig_brand, use_container_width=True)

# -------------------------------------------
# Horsepower vs Price in $
# -------------------------------------------
st.subheader("⚡ Horsepower vs Price in $")
fig_hp = px.scatter(
    filtered_df,
    x="Horsepower",
    y="Price in $",
    color="Make",
    hover_data=["Model", "Year"],
    title="Horsepower vs Price in $"
)
st.plotly_chart(fig_hp, use_container_width=True)

# -------------------------------------------
# Price in $ Distribution
# -------------------------------------------
st.subheader("💰 Price in $ Distribution")
fig_price_in_dollar = px.histogram(
    filtered_df,
    x="Price in $",
    nbins=40,
    title="Car Price in $ Distribution"
)
st.plotly_chart(fig_price_in_dollar, use_container_width=True)

# -------------------------------------------
# Average Price in $ per Brand
# -------------------------------------------
st.subheader("📊 Average Price in $ by Brand")
avg_price_in_dollar = filtered_df.groupby("Make")["Price in $"].mean().reset_index()
fig_avg = px.bar(
    avg_price_in_dollar,
    x="Make",
    y="Price in $",
    title="Average Car Price in $ by Brand",
    text_auto=True
)
st.plotly_chart(fig_avg, use_container_width=True)

# -------------------------------------------
# Fuel Efficiency (kmpl)
# -------------------------------------------
if "City kmpl" in df.columns and "Highway kmpl" in df.columns:
    st.subheader("⛽ Fuel Efficiency")
    fig_fuel = px.box(
        filtered_df,
        x="Make",
        y="City kmpl",
        title="City Fuel Efficiency (kmpl) by Brand"
    )
    st.plotly_chart(fig_fuel, use_container_width=True)

# -------------------------------------------
# Cars within Budget
# -------------------------------------------
st.subheader("🚙 Cars You Can Buy Within Your Budget")
st.dataframe(
    filtered_df[["Make", "Model", "Year", "Horsepower", "Price in $"]]
    .sort_values("Price in $")
    .head(15)
)
