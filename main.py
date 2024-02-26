import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px

negativity = []
positivity = []
dates = []
title_first = st.title("Diary Tone")
analyzer = SentimentIntensityAnalyzer()
header_first = st.subheader("Positivity")
files = ["2023-10-21.txt", "2023-10-22.txt", "2023-10-23.txt",
         "2023-10-24.txt", "2023-10-25.txt", "2023-10-26.txt",
         "2023-10-27.txt"]
for f in files:
    with open(f"texts/{f}", 'r') as file:
        text = file.read()
        score = analyzer.polarity_scores(text)
        negativity.append(score["neg"])
        positivity.append(score["pos"])
        date = f.strip('.txt')
        dates.append(date)
fig = px.line(x=dates, y=positivity,
              labels={"x": "Date", "y": "Positivity"})
st.plotly_chart(fig)

header_second = st.subheader("Negativity")

fig = px.line(x=negativity, y=dates,
              labels={"x": "Negativity", "y": "Date"})
st.plotly_chart(fig)