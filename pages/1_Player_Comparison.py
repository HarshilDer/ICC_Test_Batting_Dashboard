import streamlit as st
import plotly.express as px
import pandas as pd
from logic import load_and_clean_data

# The exact path to your dataset
FILE_PATH = "/Users/harshil/PycharmProjects/ICC_Test_Dashboard/data/ICC Test Bat 3001.xlsx"

st.set_page_config(page_title="Compare Players", layout="wide", page_icon="⚔️")

# Load the data
try:
    df = load_and_clean_data(FILE_PATH)
except Exception as e:
    st.error("Error loading data. Make sure your path is correct.")
    st.stop()

st.title("⚔️ Head-to-Head Player Comparison")
st.markdown("Filter by team, or leave it on **All Teams** and just **type a name in the Player box to search!**")

# --- TEAM & PLAYER SELECTION ---
# Get a clean list of all unique teams, and add "All Teams" at the very top
all_teams = ["All Teams"] + sorted(df['Team'].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Competitor 1")
    # 1. Select Team
    team1 = st.selectbox("🌍 Filter by Team", options=all_teams, index=0, key="t1")

    # 2. Filter players based on Team 1
    if team1 == "All Teams":
        team1_players = sorted(df['Player'].unique())
    else:
        team1_players = sorted(df[df['Team'] == team1]['Player'].unique())

    default_p1 = "SR Tendulkar (INDIA)" if "SR Tendulkar (INDIA)" in team1_players else team1_players[0]

    # 3. Select Player (This acts as a search bar!)
    player1 = st.selectbox("🏏 Search/Select Player", options=team1_players,
                           index=team1_players.index(default_p1) if default_p1 in team1_players else 0, key="p1")

with col2:
    st.markdown("### 🔵 Competitor 2")
    # 1. Select Team
    team2 = st.selectbox("🌍 Filter by Team", options=all_teams, index=0, key="t2")

    # 2. Filter players based on Team 2
    if team2 == "All Teams":
        team2_players = sorted(df['Player'].unique())
    else:
        team2_players = sorted(df[df['Team'] == team2]['Player'].unique())

    default_p2 = "RT Ponting (AUS)" if "RT Ponting (AUS)" in team2_players else team2_players[0]

    # 3. Select Player (This acts as a search bar!)
    player2 = st.selectbox("🏏 Search/Select Player", options=team2_players,
                           index=team2_players.index(default_p2) if default_p2 in team2_players else 0, key="p2")

# Filter the dataframe for only these two selected players
compare_df = df[df['Player'].isin([player1, player2])]

if len(compare_df) > 0:
    st.divider()  # Adds a nice visual separator line

    # --- COMPARISON TABLE ---
    st.subheader("📋 Head-to-Head Stats Table")

    # Select relevant stats to compare
    stats_to_compare = compare_df[['Player', 'Mat', 'Runs', 'Avg', '100', '50', 'HS_Numeric']]

    # Transpose so players are columns (easier to read)
    transposed_df = stats_to_compare.set_index('Player').T
    st.dataframe(transposed_df, use_container_width=True)

    # --- BAR GRAPHS ---
    st.subheader("📊 Visual Comparison")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Total Runs Chart
        fig_runs = px.bar(
            compare_df,
            x='Player', y='Runs', color='Player',
            title="Total Career Runs", text='Runs',
            template="plotly_dark", color_discrete_sequence=["#FF4B4B", "#0068C9"]
        )
        st.plotly_chart(fig_runs, use_container_width=True)

    with chart_col2:
        # Milestones Grouped Chart
        melted_df = compare_df.melt(id_vars='Player', value_vars=['Avg', '100', '50'],
                                    var_name='Statistic', value_name='Value')

        fig_milestones = px.bar(
            melted_df,
            x='Statistic', y='Value', color='Player', barmode='group',
            title="Average & Milestones", text='Value',
            template="plotly_dark", color_discrete_sequence=["#FF4B4B", "#0068C9"]
        )
        st.plotly_chart(fig_milestones, use_container_width=True)

else:
    st.warning("Could not load data for the selected players.")