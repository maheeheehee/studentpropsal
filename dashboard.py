import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="BRI-MH Dashboard", layout="wide")

st.title("BRI-MH: Behavioral Risk Index for Mental Health")

# -----------------------------
# Example weekly data for one user
# -----------------------------
weeks = pd.date_range("2025-07-01", periods=8, freq="W")
risk_scores = [0.32, 0.41, 0.45, 0.60, 0.52, 0.68, 0.72, 0.65]
df = pd.DataFrame({"Week": weeks, "BRI Score": risk_scores})

# Risk contributions (last week)
contributions = {
    "Mobility Reduction": 0.30,
    "Negative Sentiment": 0.40,
    "Poor Sleep": 0.20,
    "Mood Check-ins": 0.10,
}
contrib_df = pd.DataFrame(list(contributions.items()), columns=["Factor", "Contribution"])

# Mock cognitive stressors
stressor_list = ["Work stress", "Insomnia", "Family conflict", "Social withdrawal", "Financial worries"]

last_score = df["BRI Score"].iloc[-1]

# -----------------------------
# Tabs for dashboards
# -----------------------------
tab1, tab2, tab3 = st.tabs(["User Dashboard", "Clinician Dashboard", "Clinician Panel"])

# ---------------- USER DASHBOARD ----------------
with tab1:
    st.markdown("### User Dashboard")

    # --- Top row: summary cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Average Steps / Day", value="2,100", delta="-20% vs last week")
    col2.metric(label="Average Sleep", value="5h 10m", delta="-1h 30m")
    col3.metric(label="Mood Rating", value="2.3 / 5", delta="-0.7")

    # --- Risk trend chart (line with markers for grayscale) ---
    line_chart = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=80, shape="square"), strokeDash=[5,2], color="black")
        .encode(
            x=alt.X("Week:T", title="Week"),
            y=alt.Y("BRI Score:Q", title="Risk Index", scale=alt.Scale(domain=[0,1])),
        )
        .properties(width=600, height=280, title="Behavioral Risk Index (Weekly Trend)")
        .configure_axis(grid=True, gridColor="#d9d9d9")
        .configure_view(strokeWidth=0)
        .configure_title(fontSize=14, color="black")
    )
    st.altair_chart(line_chart, use_container_width=True)

    # --- Insights ---
    st.markdown("#### Insights")
    st.markdown(
        """
        - **Mobility** dropped significantly this week (avg. 2,100 steps/day).  
        - **Sleep duration** decreased by 1.5 hours compared to last week.  
        - **Mood check-ins** show lower ratings with frequent *tired* or *sad* entries.  
        """
    )

    # --- Recommendations ---
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

    # Put chart in a centered column layout
    left, center, right = st.columns([1, 2, 1])  # middle col is wider
    with center:
        bar_chart = (
            alt.Chart(contrib_df)
            .mark_bar(color="gray")
            .encode(
                x=alt.X("Contribution:Q", title="Contribution (Proportion)"),
                y=alt.Y("Factor:N", sort="-x", title="Risk Factor"),
                tooltip=["Factor", "Contribution"],
            )
            .properties(width=400, height=250, title="Risk Contribution Breakdown")
            .configure_axis(grid=True, gridColor="#d9d9d9")
            .configure_view(strokeWidth=0)
            .configure_title(fontSize=14, color="black")
        )
        st.altair_chart(bar_chart, use_container_width=False)

    # --- Risk status under the chart ---
    st.markdown("---")  # nice separator

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

    # Mock patient list
    np.random.seed(42)
    patients = [f"Patient {i}" for i in range(1, 11)]
    bri_scores = np.round(np.random.uniform(0.2, 0.9, len(patients)), 2)
    status = ["High" if s > 0.7 else "Moderate" if s > 0.5 else "Stable" for s in bri_scores]
    patient_df = pd.DataFrame({"Patient": patients, "BRI Score": bri_scores, "Status": status})

    # Table (text-only for grayscale clarity)
    st.table(patient_df)

    # Histogram with grayscale shading
    dist_chart = (
        alt.Chart(patient_df)
        .mark_bar(color="gray")
        .encode(
            x=alt.X("BRI Score:Q", bin=alt.Bin(maxbins=10), title="BRI Score"),
            y=alt.Y("count()", title="Number of Patients"),
            tooltip=["count()"],
        )
        .properties(width=600, height=300, title="Distribution of BRI Scores Across Patients")
        .configure_axis(grid=True, gridColor="#d9d9d9")
        .configure_view(strokeWidth=0)
        .configure_title(fontSize=14, color="black")
    )
    st.altair_chart(dist_chart, use_container_width=True)
