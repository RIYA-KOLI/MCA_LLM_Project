# pages/2_GitHub.py

import streamlit as st

st.set_page_config(
    page_title="GitHub Dashboard",
    page_icon="⚫",
    layout="wide"
)

st.title("⚫ GitHub Dashboard")

st.markdown("---")

username = st.text_input(
    "GitHub Username"
)

if username:

    st.success(
        f"Connected as {username}"
    )

    st.metric(
        "Repositories",
        "0"
    )

st.info(
    "GitHub API integration coming next."
)