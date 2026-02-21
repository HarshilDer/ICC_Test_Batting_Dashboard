# 🏏 Historic Test Cricket Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://icctestbattingdashboard.streamlit.app/)

Welcome to the **Historic Test Cricket Analytics Dashboard**! This interactive data web application explores over a century of Test Cricket batting statistics. It allows users to compare legendary players head-to-head and dive deep into country-level historical dominance using advanced, dynamic visualizations.

## 🌟 Features
* **Head-to-Head Player Comparison:** Dynamically search and compare any two players in Test history side-by-side using interactive charts for Runs, Centuries, and Averages.
* **The "Inception" Treemap:** A multi-level, interactive Plotly Treemap. Click on a country's block to smoothly zoom in and see the individual run contributions of every player from that nation!
* **Interactive Drill-Downs:** Powered by Streamlit's state-of-the-art `on_select` capabilities. Click on a country's bar in the charts to instantly fetch and display their full historical player roster.
* **Dynamic User Controls:** Users can change what the size and color of the Treemap boxes represent (e.g., changing size to "100s" and color to "Batting Average") via live dropdowns.

## 🛠️ Technologies Used
* **Python 3.x**
* **Streamlit:** UI Framework, multi-page routing, and session state management.
* **Plotly Express:** Interactive charting and multi-level hierarchical treemaps.
* **Pandas:** Data ingestion, cleaning, and complex aggregations.

---

## 🗺️ Project Roadmap: How I Built This

**Step 1: Data Ingestion & Cleaning (`logic.py`)**
I started by building a robust data pipeline. The raw Excel data had messy text artifacts (like asterisks indicating 'Not Out' or active players). I used Pandas string manipulation to strip these characters, converted columns (Runs, Innings, 100s) to strict numeric data types, and handled edge cases to ensure the analytics wouldn't break.

**Step 2: Architecture & Multi-Page Setup (`app.py`)**
Instead of a single cluttered dashboard, I structured the application using Streamlit's Multi-Page setup. The root `app.py` serves as the landing page introducing the dataset, while the `pages/` directory handles specific, focused analytical views.

**Step 3: Player Comparison Logic (`pages/1_Player_Comparison.py`)**
I implemented dynamic dropdown widgets that pull unique player names directly from the cleaned dataframe. I then filtered the dataset based on user selections and plotted side-by-side comparisons using Plotly, giving users immediate visual feedback on player stats.

**Step 4: Advanced Visuals & Interactivity (`pages/2_Team_Leaderboards.py`)**
To demonstrate my understanding of hierarchical data, I grouped the dataset by 'Team' to calculate historical aggregates. 
* I built a multi-level Plotly Treemap (`path=['World', 'Team', 'Player']`) allowing users to zoom from a global view down to an individual player.
* I utilized Streamlit's native `on_select="rerun"` parameter on the Bar Charts, enabling a true "drill-down" feature where clicking a specific team's bar captures the event and dynamically renders a dataframe of all players from that specific team.