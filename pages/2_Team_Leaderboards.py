import streamlit as st
import plotly.express as px
import pandas as pd
from logic import load_and_clean_data

# The exact path to your dataset
FILE_PATH = "data/ICC Test Bat 3001.xlsx"

st.set_page_config(page_title="Team Leaderboards", layout="wide", page_icon="🏆")

# Load the data
try:
    df = load_and_clean_data(FILE_PATH)
except Exception as e:
    st.error("Error loading data. Make sure your path is correct.")
    st.stop()

st.title("🏆 Country & Team Leaderboards")
st.markdown("Discover which nations have historically dominated Test Cricket.")

# --- DATA AGGREGATION (For the Bar Charts) ---
team_stats = df.groupby('Team').agg(
    Total_Runs=('Runs', 'sum'),
    Total_100s=('100', 'sum'),
    Total_50s=('50', 'sum'),
    Total_Innings=('Inn', 'sum'),
    Total_NO=('NO', 'sum'),
    Total_Players=('Player', 'count')
).reset_index()

team_stats['Total_Outs'] = team_stats['Total_Innings'] - team_stats['Total_NO']
team_stats['Historic_Average'] = team_stats.apply(
    lambda x: x['Total_Runs'] / x['Total_Outs'] if x['Total_Outs'] > 0 else 0, axis=1
).round(2)

team_stats = team_stats[team_stats['Total_Runs'] > 5000]

# --- 🌟 THE PORTFOLIO TREEMAP (Dynamic Drill-Down) ---
st.subheader("🗺️ The 'Inception' Treemap (Dynamic Drill-Down)")
st.markdown(
    "**(👆 Click on a country's block to zoom in and see the players inside it! Click the top banner to zoom back out.)**")

# Dropdowns to let the user control the chart
col_tree1, col_tree2 = st.columns(2)
with col_tree1:
    size_metric = st.selectbox("📏 Box Size Represents:", ['Runs', '100', '50', 'Mat'], index=0)
with col_tree2:
    color_metric = st.selectbox("🎨 Box Color Represents:", ['Avg', 'HS_Numeric', '100', 'Runs'], index=0)

# Filter out players with 0 in the size metric (Plotly Treemaps crash if a box size is 0)
tree_df = df[df[size_metric] > 0].copy()

# Build the interactive Treemap
fig_tree = px.treemap(
    tree_df,
    path=[px.Constant("🌍 World"), 'Team', 'Player'],  # This creates the nesting effect!
    values=size_metric,
    color=color_metric,
    hover_name='Player',
    color_continuous_scale='Plasma',
    template="plotly_dark"
)

# UI Polish: Make it big and remove messy margins
fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10), height=650)
st.plotly_chart(fig_tree, use_container_width=True)

st.divider()

# --- BAR CHARTS (Centuries & Average) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💯 Most Test Centuries")
    st.markdown("**(👆 Click any bar to see that team's player roster below!)**")
    top_100s = team_stats.sort_values(by='Total_100s', ascending=False)

    fig_100s = px.bar(
        top_100s,
        x='Team', y='Total_100s',
        text='Total_100s', color='Team',
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_100s.update_traces(textposition='outside')

    # MAGIC HAPPENS HERE: on_select="rerun" captures the user's click!
    bar_event = st.plotly_chart(fig_100s, use_container_width=True, on_select="rerun", key="bar_clicks")

with col2:
    st.subheader("📈 Highest Historic Batting Average")
    top_avg = team_stats.sort_values(by='Historic_Average', ascending=False)

    fig_avg = px.bar(
        top_avg,
        x='Team', y='Historic_Average',
        text='Historic_Average', color='Team',
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_avg.update_traces(textposition='outside')
    fig_avg.update_layout(yaxis=dict(range=[20, top_avg['Historic_Average'].max() + 5]))
    st.plotly_chart(fig_avg, use_container_width=True)

# --- DYNAMIC PLAYER ROSTER (Triggered by click) ---
st.divider()

if bar_event and len(bar_event['selection']['points']) > 0:
    clicked_team = bar_event['selection']['points'][0]['x']
    st.subheader(f"🏏 All Players for {clicked_team}")

    team_players_df = df[df['Team'] == clicked_team].sort_values(by='Runs', ascending=False)
    st.dataframe(team_players_df, use_container_width=True)
else:
    st.info(
        "👆 Click on any country's bar in the 'Most Test Centuries' chart above to see their full player roster here!")