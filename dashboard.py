import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

st.title("🧠 BRI-MH: Behavioral Risk Index for Mental Health")

# Example weekly data
weeks = pd.date_range("2025-07-01", periods=8, freq="W")
risk_scores = [0.32, 0.41, 0.45, 0.60, 0.52, 0.68, 0.72, 0.65]
df = pd.DataFrame({"Week": weeks, "BRI Score": risk_scores})

# Risk contributions (last week)
contributions = {
    "Low Mobility": 0.30,
    "Negative Sentiment": 0.40,
    "Poor Sleep": 0.20,
    "Mood Check-ins": 0.10,
}
contrib_df = pd.DataFrame(list(contributions.items()), columns=["Factor", "Contribution"])

# Mock cognitive stressors
stressor_text = "work stress, insomnia, family conflict, social withdrawal, financial worries"
stressor_list = stressor_text.split(", ")

# Split layout: User vs Clinician
col1, col2 = st.columns(2)

# ---------------- USER DASHBOARD ----------------
with col1:
    st.subheader("👤 User Dashboard")
    
    # Risk trend chart
    line_chart = (
        alt.Chart(df)
        .mark_line(point=True, color="#1f77b4")
        .encode(x="Week:T", y="BRI Score:Q")
        .properties(width=350, height=250, title="Weekly Risk Trend")
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Feedback
    last_score = df["BRI Score"].iloc[-1]
    if last_score > 0.7:
        st.error("⚠️ High risk detected. We recommend reaching out for support and maintaining a consistent sleep schedule.")
    elif last_score > 0.5:
        st.warning("⚠️ Moderate increase in risk. Reduced activity and negative journal entries contributed.")
    else:
        st.success("✅ Stable risk. Keep maintaining healthy routines!")

# ---------------- CLINICIAN DASHBOARD ----------------
with col2:
    st.subheader("👩‍⚕️ Clinician Dashboard")
    
    # Contribution bar chart
    bar_chart = (
        alt.Chart(contrib_df)
        .mark_bar(color="#ff7f0e")
        .encode(x="Contribution:Q", y=alt.Y("Factor:N", sort="-x"))
        .properties(width=350, height=250, title="Risk Contribution Breakdown")
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # Alert box
    if last_score > 0.7:
        st.error("🚨 Alert: Patient’s BRI is 0.72 (High Risk). Top contributors: Negative Sentiment, Low Mobility.")
    else:
        st.info(f"Patient’s BRI this week: {last_score:.2f}")

    # Stressor mock-up
    st.markdown("**Detected Cognitive Stressors:**")
    st.write(", ".join(stressor_list))
