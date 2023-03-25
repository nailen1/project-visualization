import altair as alt
import streamlit as st
from vega_datasets import data
import pandas as pd
import plotly.express as px

df = pd.read_csv('./database/auction-items-nonan.csv')

fig = px.scatter(
    df,
    x="number_miss",
    y="price_estimate",
    color="address_sido",
    hover_name="case_number",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)
