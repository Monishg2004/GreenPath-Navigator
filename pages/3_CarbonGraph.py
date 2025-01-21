import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from managed_db import *

def gradient_text(text, color1, color2):
    gradient_css = f"""
        background: -webkit-linear-gradient(left, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 42px;
    """
    return f'<span style="{gradient_css}">{text}</span>'

color1 = "#0d3270"
color2 = "#0fab7b"
text = "Carbon Graph"

styled_text = gradient_text(text, color1, color2)
st.write(f"<div>{styled_text}</div>", unsafe_allow_html=True)

st.write("Illuminating global carbon footprints through interactive data visualizations.")

df = pd.read_csv("data/carbonfootprint_countries.csv")
st.dataframe(df)

freq_df = pd.read_csv("data/countries_dataset.csv")
st.bar_chart(freq_df['count'])

df['Region'].value_counts().plot(kind='bar')
if st.checkbox("Area Chart"):
    all_columns = df.columns.to_list()
    feat_choices = st.multiselect("Choose a Feature", all_columns)
    new_df = df[feat_choices]
    st.area_chart(new_df)


