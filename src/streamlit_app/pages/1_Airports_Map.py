import streamlit as st
import pandas as pd

# Define Header
st.title("Airports Around the World")

# Initialize Connection to Database
conn = st.connection("mysql", type="sql")

# Airports Count by Country
st.header("Airports Count by Country")

# Perform query
df = conn.query("SELECT COUNT(1) AS 'Total Airports', country AS 'Country' FROM airports GROUP BY country ORDER BY COUNT(1) DESC;", ttl=600)

st.dataframe(df, width=3000, hide_index = True)

df2 = pd.read_csv("/Users/matthieukhl/Documents/dstairlines/data/raw/airports_data.csv")

st.map(df2)