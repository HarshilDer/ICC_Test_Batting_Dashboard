import pandas as pd
import streamlit as st


@st.cache_data
def load_and_clean_data(file_path):
    df = pd.read_excel(file_path)

    df.columns = df.columns.astype(str).str.strip()

    if 'Player' in df.columns:
        df['Player'] = df['Player'].astype(str).str.strip()

        # NEW: Extract the Team name from inside the parentheses
        # e.g., "SR Tendulkar (INDIA)" -> "INDIA"
        df['Team'] = df['Player'].str.extract(r'\((.*?)\)')[0]

        # Clean up tags like "ICC/SA" so it just says "SA"
        df['Team'] = df['Team'].str.replace('ICC/', '', regex=False)
        df['Team'] = df['Team'].str.replace('1', '', regex=False)  # cleans random numbers
        df['Team'] = df['Team'].str.strip()

    df = df.loc[:, ~df.columns.str.lower().str.contains('^unnamed|nan', na=False)]
    df = df.loc[:, ~df.columns.duplicated()]

    if 'Span' in df.columns:
        df[['Start_Year', 'End_Year']] = df['Span'].astype(str).str.split('-', expand=True).astype(int)

    cols_to_fix = ['Runs', 'Mat', 'Inn', '100', '50', 'Avg', 'NO']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('-', '0'), errors='coerce').fillna(0)

    if 'HS' in df.columns:
        df['HS_Numeric'] = df['HS'].astype(str).str.replace('*', '', regex=False)
        df['HS_Numeric'] = pd.to_numeric(df['HS_Numeric'], errors='coerce').fillna(0)

    return df