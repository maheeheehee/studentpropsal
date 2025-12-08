import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

# -------------------------------------------------------
# GLOBAL UI CSS (DOES NOT TOUCH CHARTS)
# -------------------------------------------------------
st.markdown("""
<style>

html, body, p, div, span, label, h1, h2, h3, h4, h5, h6,
table, th, td, [data-testid="stMetricValue"],
[data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
    font-size: 1.2vw !important;
    color: black !important;
}

/* VERY IMPORTANT — do NOT scale chart internals */
.vega-embed * {
    font-size: initial !important;
}

.stTabs [role="tab"] {
    font-size: 18px !important;
    padding: 8px 16px !important;
    color: black !important;
}

.stTabs [role="tab"][aria-selected="true"] {
    font-size: 20px !important;
    font-weight: bold !important;
    border-bottom: 3px solid black !important;
}

</style>
""", unsafe_allow_html=True)


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

contrib_df = pd.DataFrame(list(contributions.items()),
                          columns=["Factor", "Contribution"])

stressor_list = ["Work stress", "Insomnia", "Family conflict",
                 "Social withdrawal", "Financial worries"]

last_score = df["BRI Score"].iloc[-1]

# -------------------------------------------------------
# TABS
# -------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "User Dashboard",
    "Clinician Dashboard",
    "Clinician Panel"
])



# -------------------------------------------------------
# USER DASHBOARD
# -------------------------------------------------------
with tab1:
    st.markdown("### User Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Steps / Day", "2,100", "-20% vs last week")
    col2.metric("Average Sleep", "5h 10m", "-1h 30m")
    col3.metric("Mood Rating", "2.3 / 5", "-0.7")

    # LARGE TREND CHART
    line_chart = (
        alt.Chart(df)
        .mark_line(
            point=alt.OverlayMarkDef(size=150, filled=True),
            strokeDash=[5, 2],
            color="black"
        )
        .encode(
            x=alt.X("Week:T", title="Week",
                    axis=alt.Axis(labelFontSize=16, titleFontSize=18)),
            y=alt.Y("BRI Score:Q", title="BRI Score",
                    scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(labelFontSize=16, titleFontSize=18)),
        )
        .properties(width=800, height=300,
                    title=alt.TitleParams(
                        "Behavioral Risk Index (Weekly Trend)",
                        fontSize=24
                    ))
    )

    st.altair_chart(line_chart, use_container_width=False)

    st.markdown("#### Insights")
    st.markdown("""
    - Mobility dropped significantly  
    - Sleep decreased by 1.5 hours  
    - Mood check-ins show tired / sad entries  
    """)



# -------------------------------------------------------
# CLINICIAN DASHBOARD — FIXED LARGE ALTAR BAR CHART
# -------------------------------------------------------
with tab2:

    st.markdown("### Clinician Dashboard")

    # =================== THE BIG BAR CHART ===================
    bar_chart = (
        alt.Chart(contrib_df)
        .mark_bar(size=70, color="gray")
        .encode(
            y=alt.Y(
                "Factor:N",
                sort="-x",
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=20,
                    titleFontSize=22,
                    labelColor="black",
                    titleColor="black"
                ),
                title="Risk Factor"
            ),
            x=alt.X(
                "Contribution:Q",
                axis=alt.Axis(
                    labelFontSize=20,
                    titleFontSize=22,
                    labelColor="black",
                    titleColor="black"
                ),
                title="Contribution (Proportion)"
            )
        )
        .properties(
            width=900,      # <<-- BIG WIDTH
            height=450,     # <<-- BIG HEIGHT
            padding={"left": 150},
            title=alt.TitleParams(
                "Risk Contribution Breakdown",
                fontSize=28,
                color="black"
            )
        )
        .configure_view(strokeWidth=0)
    )

    # Render WITHOUT Streamlit auto-resizing
    st.altair_chart(bar_chart, use_container_width=False)

    st.markdown("---")

    if last_score > 0.7:
        st.header("Risk Status: HIGH")
    elif last_score > 0.5:
        st.header("Risk Status: MODERATE")
    else:
        st.header("Risk Status: STABLE")

    st.subheader(f"BRI Score = {last_score:.2f}")

    st.subheader("Detected Cognitive Stressors:")
    st.write(", ".join(stressor_list))



# -------------------------------------------------------
# CLINICIAN PANEL
# -------------------------------------------------------
with tab3:

    st.markdown("### Multi-Patient Overview")

    np.random.seed(42)
    patients = [f"Patient {i}" for i in range(1, 11)]
    bri_scores = np.round(np.random.uniform(0.2, 0.9, len(patients)), 2)
    status = ["High" if s > 0.7 else "Moderate" if s > 0.5 else "Stable"
              for s in bri_scores]

    st.table(pd.DataFrame({
        "Patient": patients,
        "BRI Score": bri_scores,
        "Status": status
    }))
