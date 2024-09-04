import streamlit as st
import pandas as pd
import os
import pydeck as pdk

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

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df2,
                pickable=True,
                stroked=True,
                filled=True,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius= 1000,
                radius_scale=2 * 11,
                radis_min_pixels=5,
                radius_max_pixels=10,
            ),
        ],
        tooltip={"text": "{name} {iata}"}
    )
)