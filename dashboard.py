import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

# -------------------------------------------------------
# GLOBAL CSS — EXTREME LARGE TEXT FOR EVERYTHING
# -------------------------------------------------------
st.markdown(
    """
    <style>
    /* Unified moderate-large text everywhere */
    html, body, p, div, span, label, h1, h2, h3, h4, h5, h6,
    table, th, td, [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
        font-size: 1.4vw !important;   /* Perfect readable size */
        line-height: 1.2 !important;
    }

    /* Remove big Streamlit padding to avoid scrolling */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Prevent charts from overflowing → fit screen width */
    .vega-embed, canvas {
        max-width: 100% !important;
        height: auto !important;
    }

    /* Force tabs to not expand vertically */
    .stTabs [role="tablist"] button {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("BRI-MH: Behavioral Risk Index for Mental Health")

# -----------------------------
# Example weekly data
# -----------------------------
weeks = pd.date_range("2025-07-01", periods=8, freq="W")
risk_scores = [0.32, 0.41, 0.45, 0.60, 0.52, 0.68, 0.72, 0.65]
df = pd.DataFrame({"Week": weeks, "BRI Score": risk_scores})

contributions = {
    "Mobility Reduction": 0.30,
    "Negative Sentiment": 0.40,
    "Poor Sleep": 0.20,
    "Mood Check-ins": 0.10,
}
contrib_df = pd.DataFrame(list(contributions.items()), columns=["Factor", "Contribution"])

stressor_list = ["Work stress", "Insomnia", "Family conflict", "Social withdrawal", "Financial worries"]

last_score = df["BRI Score"].iloc[-1]

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["User Dashboard", "Clinician Dashboard", "Clinician Panel"])

# ---------------- USER DASHBOARD ----------------
with tab1:
    st.markdown("### User Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Average Steps / Day", value="2,100", delta="-20% vs last week")
    col2.metric(label="Average Sleep", value="5h 10m", delta="-1h 30m")
    col3.metric(label="Mood Rating", value="2.3 / 5", delta="-0.7")

    # Line Chart (Large fonts)
    line_chart = (
        alt.Chart(df)
        .mark_line(
            point=alt.OverlayMarkDef(filled=True, size=350, shape="square"),
            strokeDash=[5,2],
            color="black"
        )
        .encode(
            x=alt.X("Week:T", title="Week"),
            y=alt.Y("BRI Score:Q", title="Risk Index", scale=alt.Scale(domain=[0,1])),
        )
        .properties(width=800, height=450, title="Behavioral Risk Index (Weekly Trend)")
        .configure_axis(labelFontSize=32, titleFontSize=40)
        .configure_title(fontSize=50)
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.markdown("#### Insights")
    st.markdown("""
        - **Mobility** dropped significantly this week (avg. 2,100 steps/day).  
        - **Sleep duration** decreased by 1.5 hours compared to last week.  
        - **Mood check-ins** show lower ratings with frequent *tired* or *sad* entries.  
    """)

    st.markdown("#### Recommendation")
    if last_score > 0.7:
        st.markdown("**[HIGH RISK]** Patient should seek immediate clinical support.")
    elif last_score > 0.5:
        st.markdown("**[MODERATE RISK]** Encourage improved sleep and activity routines.")
    else:
        st.markdown("**[STABLE]** Continue consistent behavior. No immediate concerns.")

# ---------------- CLINICIAN DASHBOARD ----------------
with tab2:
    st.markdown("### Clinician Dashboard")

    col_chart, col_space = st.columns([2, 1])
    with col_chart:
        bar_chart = (
            alt.Chart(contrib_df)
            .mark_bar(size=60, color="gray")
            .encode(
                x=alt.X("Contribution:Q", title="Contribution (Proportion)"),
                y=alt.Y("Factor:N", sort="-x", title="Risk Factor"),
                tooltip=["Factor", "Contribution"],
            )
            .properties(width=650, height=400, title="Risk Contribution Breakdown")
            .configure_axis(labelFontSize=32, titleFontSize=40)
            .configure_title(fontSize=50)
        )
        st.altair_chart(bar_chart, use_container_width=True)

    st.markdown("---")

    if last_score > 0.7:
        st.markdown("#### Risk Status: **HIGH**")
        st.markdown(f"Patient BRI = {last_score:.2f}  \nMain contributors: Negative Sentiment, Reduced Mobility")
    elif last_score > 0.5:
        st.markdown("#### Risk Status: **MODERATE**")
        st.markdown(f"Patient BRI = {last_score:.2f}  \nContributors: Sleep, Mood Variability")
    else:
        st.markdown("#### Risk Status: **STABLE**")
        st.markdown(f"Patient BRI = {last_score:.2f}  \nContinue monitoring.")

    st.markdown("**Detected Cognitive Stressors:**")
    st.markdown(", ".join(stressor_list))

# ---------------- CLINICIAN PANEL ----------------
with tab3:
    st.markdown("### Multi-Patient Overview")

    np.random.seed(42)
    patients = [f"Patient {i}" for i in range(1, 11)]
    bri_scores = np.round(np.random.uniform(0.2, 0.9, len(patients)), 2)
    status = ["High" if s > 0.7 else "Moderate" if s > 0.5 else "Stable" for s in bri_scores]
    patient_df = pd.DataFrame({"Patient": patients, "BRI Score": bri_scores, "Status": status})

    st.table(patient_df)

    dist_chart = (
        alt.Chart(patient_df)
        .mark_bar(size=60, color="gray")
        .encode(
            x=alt.X("BRI Score:Q", bin=alt.Bin(maxbins=10), title="BRI Score"),
            y=alt.Y("count()", title="Number of Patients"),
        )
        .properties(width=800, height=450, title="Distribution of BRI Scores Across Patients")
        .configure_axis(labelFontSize=32, titleFontSize=40)
        .configure_title(fontSize=50)
    )
    st.altair_chart(dist_chart, use_container_width=True)
