import streamlit as st
import plotly.express as px
from logic import load_and_clean_data

# The exact path to your dataset
FILE_PATH = "data/ICC Test Bat 3001.xlsx"


def setup_sidebar(df):
    """Handles all user inputs from the sidebar and returns the filtered/sorted dataframe."""
    st.sidebar.header("Navigation & Filters")

    # 1. Search Player (using .strip() to ignore accidental spacebar hits)
    # NOTE: Search by LAST NAME (e.g., 'Tendulkar' instead of 'Sachin')
    search_query = st.sidebar.text_input("Search Player (e.g., Kohli, Root)").strip()

    # 2. Year Range
    min_yr, max_yr = int(df['Start_Year'].min()), int(df['End_Year'].max())
    year_filter = st.sidebar.slider("Career Year Range", min_yr, max_yr, (min_yr, max_yr))

    # 3. Sorting Filters
    sort_by = st.sidebar.selectbox("Sort Table By", ['Runs', 'Avg', '100', '50', 'Mat', 'HS_Numeric'])
    order = st.sidebar.radio("Direction", ["Descending", "Ascending"])

    # Apply the Year filter (Checks for ANY career overlap with selected years)
    filtered_df = df[(df['Start_Year'] <= year_filter[1]) & (df['End_Year'] >= year_filter[0])]

    # Apply the Search filter safely
    if search_query:
        filtered_df = filtered_df[filtered_df['Player'].astype(str).str.contains(search_query, case=False, na=False)]

    # Sort the final dataframe
    sorted_df = filtered_df.sort_values(by=sort_by, ascending=(order == "Ascending"))

    return sorted_df, sort_by, order


def render_visuals(sorted_df, sort_by, order):
    """Renders the charts in a two-column layout."""
    st.subheader("📊 Performance Analytics")

    # SAFETY NET: Check if the dataframe is empty after searching
    if sorted_df.empty:
        st.warning("No players found matching your search criteria. Try using just their Last Name!")
        return  # Stop drawing charts if there is no data

    col1, col2 = st.columns(2)

    with col1:
        # NEW CHART: Matches vs. Total Runs vs. Average
        st.subheader("Matches vs. Runs & Average")

        # We use a Scatter/Bubble chart to handle the massive difference between Run numbers and Match numbers
        fig_bubble = px.scatter(
            sorted_df.head(50),  # Show up to 50 players
            x='Mat',
            y='Runs',
            color='Avg',
            size='Avg',  # Higher average = larger bubble
            hover_name='Player',
            title="Matches vs. Runs (Bubble Size = Average)",
            labels={'Mat': 'Matches Played', 'Runs': 'Total Runs', 'Avg': 'Batting Average'},
            template="plotly_dark",
            color_continuous_scale="Viridis"  # A cool green/purple/yellow color scale
        )

        # Makes the dots slightly larger so they are easier to see for a single player
        fig_bubble.update_traces(marker=dict(sizemin=8))

        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        # 3D Career Explorer Chart
        st.subheader("3D Career Metrics")
        fig_3d = px.scatter_3d(
            sorted_df.head(50),  # Shows top 50 to avoid cluttering the 3D space
            x='Mat', y='Avg', z='Runs',
            color='100', hover_name='Player',
            title="Matches vs. Average vs. Total Runs",
            template="plotly_dark",
            color_continuous_scale="Plasma"
        )
        fig_3d.update_layout(height=500)  # Give the 3D chart room to rotate
        st.plotly_chart(fig_3d, use_container_width=True)


def render_table(sorted_df):
    """Renders the raw data table."""
    st.subheader("📋 Filtered Player Data")
    if not sorted_df.empty:
        st.dataframe(sorted_df, use_container_width=True)


def main():
    """Main function to run the Streamlit app."""
    # Set page config must be the first Streamlit command
    st.set_page_config(page_title="ICC Test Stats Hub", layout="wide", page_icon="🏏")

    # Load the data
    try:
        df = load_and_clean_data(FILE_PATH)
    except Exception as e:
        st.error(f"Error loading file: {e}. Check if the Excel file is open elsewhere or the path is incorrect.")
        st.stop()

    # Dashboard Header
    st.title("🏏 ICC Test Batting Dashboard (1877-2019)")

    # Execute UI Components
    sorted_df, sort_by, order = setup_sidebar(df)
    render_visuals(sorted_df, sort_by, order)
    render_table(sorted_df)


# Run the app
if __name__ == "__main__":
    main()