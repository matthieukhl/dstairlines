import streamlit as st 
import pandas as pd
import numpy as np
import os

# Set variables
current_dir = os.path.dirname(__file__)
image_dir = os.path.join(current_dir, "assets", "images")

# Configure Page
st.set_page_config(
    page_title="DST Airlines",
    page_icon=":airplane:",
    layout="wide",
    menu_items={
        "About": "https://github.com/matthieukhl/dstairlines"
    }
)

# CSS Injection
st.markdown("""
            <style>
                img {
                    border-radius: 25px
          }
        </style>
        """, unsafe_allow_html=True)

# Title and subheader
st.title("DST Airlines :airplane:")
st.subheader("Keep track of flights!")

# Columns setup
col1, col2 = st.columns(2)

# Column 1
col1.header("Discover Airporsts Around the World")
col1.write("An interactive map to discover airports all around the globe!")

# Column 2
col2.image(f"{image_dir}/airports_map.png")