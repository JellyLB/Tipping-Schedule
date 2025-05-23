import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tipping Schedule Dashboard", layout="wide")

st.title("Batch Production Tracker")

# Upload Excel file
uploaded_file = st.file_uploader("Upload the tipping schedule Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Optional: Preview data
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Filter by owner
    if 'Owner' in df.columns:
        owner_filter = st.selectbox("Filter by Owner", ["All"] + sorted(df['Owner'].dropna().unique()))
        if owner_filter != "All":
            df = df[df['Owner'] == owner_filter]

    # Status summary chart
    if 'Status' in df.columns:
        st.subheader("Batch Status Overview")
        status_counts = df['Status'].value_counts().reset_index()
        fig = px.bar(status_counts, x='index', y='Status',
                     labels={'index': 'Status'}, title="Batch Count by Status")
        st.plotly_chart(fig, use_container_width=True)

    # Gantt chart if dates available
    if 'Start Date' in df.columns and 'End Date' in df.columns:
        st.subheader("Timeline View (Gantt Chart)")
        fig2 = px.timeline(df, x_start="Start Date", x_end="End Date", y="Batch ID", color="Status")
        fig2.update_yaxes(autorange="reversed")
        st.plotly_chart(fig2, use_container_width=True)

    # Final table
    st.subheader("Full Table")
    st.dataframe(df)

else:
    st.info("Please upload a file to begin.")
