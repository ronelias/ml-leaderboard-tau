# file: app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page config
st.set_page_config(
    page_title="ML Competition Leaderboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-18e3th9 { padding: 1rem; }
    .css-1d391kg {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        padding: 2rem;
    }
    table tbody tr:nth-child(1) td {
        background-color: #ffd70033 !important;  /* Gold */
    }
    table tbody tr:nth-child(2) td {
        background-color: #c0c0c033 !important;  /* Silver */
    }
    table tbody tr:nth-child(3) td {
        background-color: #cd7f3233 !important;  /* Bronze */
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
    <h1 style='color:#003366;'>🏆 ML Competition Leaderboard</h1>
    <h4 style='color:#004488;'>BSc Digital Science – 'Introduction to ML' Course</h4>
    <h5 style='color:#555;'>Florida Dataset – Faculty of Engineering, Tel Aviv University</h5>
    <hr>
""", unsafe_allow_html=True)

# Load Data
# uploaded_file = st.file_uploader("Upload group AUC results CSV", type=["csv"], help="Must contain 'group' and 'auc' columns")

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
# else:
df = pd.read_csv("group_auc_results.csv")  # fallback default

# Sort leaderboard
df_sorted = df.sort_values(by="auc", ascending=False).reset_index(drop=True)

# Add emojis for top 3
medals = ["🥇", "🥈", "🥉"] + ["" for _ in range(len(df_sorted) - 3)]
df_sorted.insert(0, "🏅", medals)

# Statistics
mean_auc = df_sorted['auc'].mean()
median_auc = df_sorted['auc'].median()
std_auc = df_sorted['auc'].std()
high_auc_count = (df_sorted['auc'] > 0.85).sum()

st.markdown("## 📈 Competition Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average AUC", f"{mean_auc:.3f}")
col2.metric("Median AUC", f"{median_auc:.3f}")
col3.metric("Std. Deviation", f"{std_auc:.3f}")
col4.metric("Groups > 0.85", f"{high_auc_count}")

# Leaderboard
st.markdown("## 📊 Current Standings")
st.dataframe(df_sorted, use_container_width=True, height=500)

# Plot AUC scores
st.markdown("## 📉 AUC Scores by Group")
df_sorted['rank'] = df_sorted.index + 1
fig = px.bar(
    df_sorted,
    x="group",
    y="auc",
    color="auc",
    color_continuous_scale="Blues",
    title="Group AUC Performance",
    labels={"group": "Group", "auc": "AUC Score"},
    hover_data={"rank": True, "group": True, "auc": ":.3f"}
)
fig.add_hline(y=0.7, line_dash="dash", line_color="red", annotation_text="AUC = 0.7", annotation_position="top left")
fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="white", paper_bgcolor="white")
st.plotly_chart(fig, use_container_width=True)

# Additional Visualization: Distribution
st.markdown("## 📊 AUC Score Distribution")
hist_fig = px.histogram(
    df_sorted,
    x="auc",
    nbins=10,
    title="Distribution of AUC Scores",
    labels={"auc": "AUC Score"},
    color_discrete_sequence=["#1f77b4"]
)
hist_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
st.plotly_chart(hist_fig, use_container_width=True)

# Footer
st.markdown("""
    <br><br><center>
    <small>Built with ❤️ for the students of Tel Aviv University, Faculty of Engineering.</small>
    </center>
""", unsafe_allow_html=True)
