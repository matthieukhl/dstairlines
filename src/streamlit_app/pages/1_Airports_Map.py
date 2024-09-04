import streamlit as st
import pandas as pd
import os

# Define Header
st.title("Airports Around the World")

# Initialize Connection to Database
conn = st.connection("mysql", type="sql")

# Airports Count by Country
st.header("Airports Count by Country")

# Perform query
df = conn.query("SELECT COUNT(1) AS 'Total Airports', country AS 'Country' FROM airports GROUP BY country ORDER BY COUNT(1) DESC;", ttl=600)

st.dataframe(df, width=3000, hide_index = True)

# Display Airports Map
st.header("Airports Map")
current_dir = os.path.dirname(__file__) 

df2_path = os.path.join(current_dir, "..", "..", "..", "data", "raw", "airports_data.csv")
df2 = pd.read_csv(df2_path)

st.map(df2)