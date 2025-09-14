import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

st.title("🧠 BRI-MH: Behavioral Risk Index for Mental Health")

# Fake example weekly data
weeks = pd.date_range("2025-07-01", periods=8, freq="W")
risk_scores = [0.32, 0.41, 0.45, 0.60, 0.52, 0.68, 0.72, 0.65]

# Risk contributions for last week (example values)
contributions = {
    "Low Mobility": 0.30,
    "Negative Sentiment": 0.40,
    "Poor Sleep": 0.20,
    "Mood Check-ins": 0.10,
}

# Tabs for User and Clinician views
tab1, tab2 = st.tabs(["👤 User Dashboard", "👩‍⚕️ Clinician Dashboard"])

with tab1:
    st.subheader("Your Weekly Risk Index")
    
    # Plot risk trend
    fig, ax = plt.subplots()
    ax.plot(weeks, risk_scores, marker="o", linestyle="-")
    ax.axhline(0.7, color="red", linestyle="--", label="High Risk Threshold")
    ax.set_ylim(0, 1)
    ax.set_ylabel("BRI Score")
    ax.set_title("Weekly Risk Trend")
    ax.legend()
    st.pyplot(fig)

    # Simple feedback message
    last_score = risk_scores[-1]
    if last_score > 0.7:
        st.error("⚠️ Your risk level is high this week. We recommend reaching out for support and following a sleep routine.")
    elif last_score > 0.5:
        st.warning("⚠️ Your risk level increased moderately. Reduced activity and negative journal entries contributed.")
    else:
        st.success("✅ Your risk level is stable. Keep maintaining healthy routines.")

with tab2:
    st.subheader("Clinician View: Risk Breakdown")

    # Bar chart of contributions
    contrib_df = pd.DataFrame.from_dict(contributions, orient="index", columns=["Contribution"])
    contrib_df = contrib_df.sort_values("Contribution", ascending=False)

    st.bar_chart(contrib_df)

    # Alert if high risk
    if last_score > 0.7:
        st.error("🚨 Alert: Patient’s BRI is 0.72 (High Risk). Top contributors: Negative Sentiment, Low Mobility.")
    else:
        st.info(f"Patient’s BRI this week: {last_score:.2f}")

    # Table view
    st.table(contrib_df)
