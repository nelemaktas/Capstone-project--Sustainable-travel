import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    return pd.read_csv("routes.csv")

routes = load_data()

st.title("About this dataset")

st.write("This dataset was manually collected from *Rome2Rio* following a standardised rule. City pairs were chosen arbitrarily according to personal interest. Air distances were retrieved from *distance.to.org*.")
st.markdown("""
- All fares for 14 July 2026 :gray[(as if booking a trip 3 months in advance)]
- Cheapest direct connection. Consider only high-speed rail.
- All travel times must be between 6am and 10pm
- If only price span was available, look price up on train operator's website, else use the average of the price span.
""")
st.write("*Rome2Rio* and other transport-related booking platform " \
"providers also offer an API that could be used to do the same analysis on a much larger dataset. However, that API is a paid service.")

st.subheader("Explore the underlying dataset by yourself")

st.dataframe(routes)



