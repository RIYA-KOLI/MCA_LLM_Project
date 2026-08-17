# pages/3_StackExchange.py

import streamlit as st

st.set_page_config(
    page_title="StackExchange Explorer",
    page_icon="🔵",
    layout="wide"
)

st.title("🔵 StackExchange Explorer")

st.markdown("---")

query = st.text_input(
    "Search Programming Questions"
)

if query:

    st.success(
        f"Searching for: {query}"
    )

st.info(
    "StackExchange API integration coming next."
)