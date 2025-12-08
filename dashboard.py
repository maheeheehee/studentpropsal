import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

# -------------------------------------------------------
# GLOBAL CSS — Uniform Text, No Scrolling
# -------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, p, div, span, label, h1, h2, h3, h4, h5, h6,
    table, th, td, [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
        font-size: 1.4vw !important;
        line-height: 1.2 !important;
    }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .vega-embed, canvas {
        height: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------
# CHART LABEL OVERRIDES — BIG TEXT FOR SCREENSHOT
# -------------------------------------------------------
st.markdown(
    """
    <style>
    .vega-embed text {
        font-size: 36px !important;
        font-weight: 600 !important;
    }
    .vega-embed .role-axis-title {
        font-size: 40px !important;
        font-weight: 700 !important;
    }
    .vega-embed .role-axis-label {
        font-size: 36px !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------
# DATA
# -------------------------------------------------------
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

# -------------------------------------------------------
# TABS
# -------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["User Dashboard", "Clinician Dashboard", "Clinician Panel"])

# -------------------------------------------------------
# USER DASHBOARD
# -------------------------------------------------------
with tab1:
    st.markdown("### User Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Steps / Day", "2,100", "-20% vs last week")
    col2.metric("Average Sleep", "5h 10m", "-1h 30m")
    col3.metric("Mood Rating", "2.3 / 5", "-0.7")

    # Trend chart
    line_chart = (
        alt.Chart(df)
        .mark_line(
            point=alt.OverlayMarkDef(filled=True, size=200, shape="square"),
            strokeDash=[5, 2],
            color="black"
        )
        .encode(
            x=alt.X("Week:T", title="Week"),
            y=alt.Y("BRI Score:Q", title="Risk Index", scale=alt.Scale(domain=[0, 1])),
        )
        .properties(width="container", height=320, title="Behavioral Risk Index (Weekly Trend)")
        .configure_axis(labelFontSize=22, titleFontSize=26)
        .configure_title(fontSize=28)
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.markdown("#### Insights")
    st.markdown("""
        - **Mobility** dropped significantly this week.  
        - **Sleep** reduced by 1.5 hours.  
        - **Mood check-ins** show frequent tired/sad entries.  
    """)

    st.markdown("#### Recommendation")
    if last_score > 0.7:
        st.markdown("**[HIGH RISK]** Seek immediate clinical support.")
    elif last_score > 0.5:
        st.markdown("**[MODERATE RISK]** Improve sleep & mood routines.")
    else:
        st.markdown("**[STABLE]** No immediate concerns.")


# -------------------------------------------------------
# CLINICIAN DASHBOARD (FIXED)
# -------------------------------------------------------
with tab2:
    st.markdown("### Clinician Dashboard")

    # ------------------------------
    # FIXED LARGE BAR CHART
    # ------------------------------
    bar_chart = (
        alt.Chart(contrib_df)
        .mark_bar(size=120, color="gray")
        .encode(
            x=alt.X("Contribution:Q", title="Contribution (Proportion)"),
            y=alt.Y(
                "Factor:N",
                sort="-x",
                title="Risk Factor",
                axis=alt.Axis(
                    labelFontSize=36,
                    titleFontSize=40,
                    labelLimit=1000
                )
            ),
            tooltip=["Factor", "Contribution"]
        )
        .properties(
            width=1200,          # FIXED WIDTH (no compression)
            height=600,          # BIG HEIGHT (readable)
            title=alt.TitleParams(
                "Risk Contribution Breakdown",
                fontSize=42
            )
        )
        .configure_axis(
            labelFontSize=36,
            titleFontSize=40
        )
    )

    st.altair_chart(bar_chart, use_container_width=False)

    st.markdown("---")

    # Risk Status
    if last_score > 0.7:
        st.markdown("#### Risk Status: **HIGH**")
        st.markdown(f"Patient BRI = {last_score:.2f}\nMain: Negative Sentiment, Low Mobility")
    elif last_score > 0.5:
        st.markdown("#### Risk Status: **MODERATE**")
        st.markdown(f"Patient BRI = {last_score:.2f}\nContributors: Sleep, Mood Variability")
    else:
        st.markdown("#### Risk Status: **STABLE**")
        st.markdown(f"Patient BRI = {last_score:.2f}\nContinue monitoring.")

    st.markdown("**Detected Cognitive Stressors:**")
    st.markdown(", ".join(stressor_list))


# -------------------------------------------------------
# CLINICIAN PANEL
# -------------------------------------------------------
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
        .mark_bar(size=50, color="gray")
        .encode(
            x=alt.X("BRI Score:Q", bin=alt.Bin(maxbins=10), title="BRI Score"),
            y=alt.Y("count()", title="Number of Patients")
        )
        .properties(width="container", height=300, title="Distribution of BRI Scores Across Patients")
        .configure_axis(labelFontSize=22, titleFontSize=26)
        .configure_title(fontSize=28)
    )

    st.altair_chart(dist_chart, use_container_width=True)
