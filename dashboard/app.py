# dashboard/app.py
import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Fraud Dashboard")
st.title("Behavioral Biometrics — Fraud Dashboard")

CSV = os.path.join(os.path.dirname(__file__), "..", "backend", "scores.csv")

if not os.path.exists(CSV):
    st.info("No scores yet. Run backend and send some events from the frontend.")
else:
    df = pd.read_csv(CSV)
    st.subheader("Recent submissions")
    st.dataframe(df.tail(200))

    st.subheader("Risk distribution")
    st.bar_chart(df['decision'].value_counts())

    st.subheader("Risk histogram")
    st.bar_chart(pd.cut(df['risk_pct'], bins=10).value_counts().sort_index())
