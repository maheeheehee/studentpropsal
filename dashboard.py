import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

# -------------------------------------------------------
# GLOBAL CSS — LARGE UI TEXT, DOES NOT AFFECT CHARTS
# -------------------------------------------------------
st.markdown("""
<style>

html, body, p, div, span, label, h1, h2, h3, h4, h5, h6,
table, th, td, [data-testid="stMetricValue"],
[data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
    font-size: 1.3vw !important;
    color: black !important;
    line-height: 1.3 !important;
}

/* FIX TABS */
.stTabs [role="tab"] {
    font-size: 18px !important;
    padding: 6px 14px !important;
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

stressor_list = ["Work stress", "Insomnia",
                 "Family conflict", "Social withdrawal",
                 "Financial worries"]

last_score = df["BRI Score"].iloc[-1]


# -------------------------------------------------------
# TABS
# -------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["User Dashboard", "Clinician Dashboard", "Clinician Panel"]
)



# -------------------------------------------------------
# USER DASHBOARD
# -------------------------------------------------------
with tab1:
    st.markdown("### User Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Steps / Day", "2,100", "-20% vs last week")
    col2.metric("Average Sleep", "5h 10m", "-1h 30m")
    col3.metric("Mood Rating", "2.3 / 5", "-0.7")

    # ========== PLOTLY LINE CHART ==========
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df["Week"],
        y=df["BRI Score"],
        mode="lines+markers",
        marker=dict(size=12),
        line=dict(dash="dash", width=3, color="black")
    ))

    fig_line.update_layout(
        title="Behavioral Risk Index (Weekly Trend)",
        title_font_size=28,
        yaxis=dict(range=[0, 1], title="BRI Score", title_font_size=20),
        xaxis=dict(title="Week", title_font_size=20),
        height=350,
        margin=dict(l=20, r=20, t=60, b=50)
    )

    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("#### Insights")
    st.markdown("""
    - Mobility dropped significantly this week  
    - Sleep decreased by 1.5 hours  
    - Mood check-ins show more tired/sad entries  
    """)

    st.markdown("#### Recommendation")
    if last_score > 0.7:
        st.markdown("**[HIGH RISK] Seek immediate clinical support.**")
    elif last_score > 0.5:
        st.markdown("**[MODERATE RISK] Improve sleep and routine consistency.**")
    else:
        st.markdown("**[STABLE] No major concern.**")



# -------------------------------------------------------
# CLINICIAN DASHBOARD WITH PLOTLY BAR CHART
# -------------------------------------------------------
with tab2:
    st.markdown("### Clinician Dashboard")

    # ========== PLOTLY BAR CHART (BIG & CLEAR) ==========
    contrib_df = pd.DataFrame(
        list(contributions.items()),
        columns=["Factor", "Contribution"]
    )

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=contrib_df["Factor"],
        x=contrib_df["Contribution"],
        orientation="h",
        marker=dict(color="gray")
    ))

    fig_bar.update_layout(
        title="Risk Contribution Breakdown",
        title_font_size=28,
        xaxis=dict(title="Contribution (Proportion)",
                   title_font_size=22, tickfont_size=18),
        yaxis=dict(title="Risk Factor",
                   title_font_size=22, tickfont_size=18),
        height=550,
        margin=dict(l=180, r=40, t=60, b=60)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    if last_score > 0.7:
        st.markdown("### Risk Status: **HIGH**")
    elif last_score > 0.5:
        st.markdown("### Risk Status: **MODERATE**")
    else:
        st.markdown("### Risk Status: **STABLE**")

    st.markdown(f"Patient BRI = **{last_score:.2f}**")
    st.markdown("**Detected Cognitive Stressors:**")
    st.markdown(", ".join(stressor_list))



# -------------------------------------------------------
# CLINICIAN PANEL
# -------------------------------------------------------
with tab3:
    st.markdown("### Multi-Patient Overview")

    np.random.seed(42)
    patients = [f"Patient {i}" for i in range(1, 11)]
    bri_scores = np.round(np.random.uniform(0.2, 0.9, 10), 2)
    status = ["High" if s > 0.7 else "Moderate" if s > 0.5 else "Stable"
              for s in bri_scores]

    st.table(pd.DataFrame({
        "Patient": patients,
        "BRI Score": bri_scores,
        "Status": status
    }))

    # Histogram
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=bri_scores,
        nbinsx=10,
        marker=dict(color="gray")
    ))

    fig_hist.update_layout(
        title="Distribution of BRI Scores Across Patients",
        title_font_size=26,
        xaxis=dict(title="BRI Score", title_font_size=20),
        yaxis=dict(title="Count", title_font_size=20),
        height=350
    )

    st.plotly_chart(fig_hist, use_container_width=True)
