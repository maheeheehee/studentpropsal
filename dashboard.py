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
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["User Dashboard", "Clinician Dashboard", "Clinician Panel"])

# ---------------- USER DASHBOARD ----------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Weekly Behavioral Risk Index")

        # Summary card
        st.markdown(
            f"""
            <div style="padding:15px; border-radius:10px; border:1px solid #ccc; background-color:#f9f9f9;">
            <h4 style="margin:0;">Current Score</h4>
            <p style="font-size:22px; font-weight:bold; color:{'red' if last_score>0.7 else 'orange' if last_score>0.5 else 'green'};">
            {last_score:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        # Line chart
        line_chart = (
            alt.Chart(df)
            .mark_line(point=True, strokeWidth=3, color="#1f77b4")
            .encode(
                x=alt.X("Week:T", title="Week"),
                y=alt.Y("BRI Score:Q", title="Risk Index", scale=alt.Scale(domain=[0,1])),
            )
            .properties(width=350, height=250, title="Risk Trend")
        )
        st.altair_chart(line_chart, use_container_width=True)

    # Feedback
    if last_score > 0.7:
        st.markdown("**Status:** High risk. Recommend clinician follow-up and intervention.")
    elif last_score > 0.5:
        st.markdown("**Status:** Moderate increase in risk. Monitor closely.")
    else:
        st.markdown("**Status:** Stable. No immediate concerns.")

# ---------------- CLINICIAN DASHBOARD ----------------
with tab2:
    st.markdown("### Single Patient Risk Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        # Contributions
        bar_chart = (
            alt.Chart(contrib_df)
            .mark_bar(color="#ff7f0e")
            .encode(
                x=alt.X("Contribution:Q", title="Contribution (Proportion)"),
                y=alt.Y("Factor:N", sort="-x", title="Risk Factor"),
            )
            .properties(width=350, height=250, title="Risk Contribution Breakdown")
        )
        st.altair_chart(bar_chart, use_container_width=True)

    with col2:
        # Alert card
        if last_score > 0.7:
            st.markdown(
                """
                <div style="padding:15px; border-radius:10px; border:1px solid #ccc; background-color:#ffe6e6;">
                <h4 style="margin:0; color:#b30000;">Alert: High Risk</h4>
                <p style="margin:0;">Patient’s Behavioral Risk Index is 0.72. 
                Major contributors: Negative Sentiment and Reduced Mobility.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="padding:15px; border-radius:10px; border:1px solid #ccc; background-color:#f2f2f2;">
                <h4 style="margin:0; color:#333;">Risk Status</h4>
                <p style="margin:0;">Patient’s Behavioral Risk Index is {last_score:.2f}. 
                Continue monitoring for changes.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

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

    # Table view
    st.dataframe(patient_df.style.apply(
        lambda x: ["background-color: #ffe6e6" if v=="High" else "background-color: #fff4e6" if v=="Moderate" else "background-color: #e6ffe6" for v in x],
        subset=["Status"]
    ))

    # Distribution chart
    dist_chart = (
        alt.Chart(patient_df)
        .mark_bar()
        .encode(
            x=alt.X("BRI Score:Q", bin=alt.Bin(maxbins=10)),
            y="count()",
            color=alt.Color("Status:N", scale=alt.Scale(domain=["High","Moderate","Stable"], range=["#b30000","#ff7f0e","#1f77b4"]))
        )
        .properties(width=600, height=300, title="Distribution of BRI Scores Across Patients")
    )
    st.altair_chart(dist_chart, use_container_width=True)
