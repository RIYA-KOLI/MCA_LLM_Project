# pages/1_LeetCode.py

import streamlit as st
from utils.leetcode_service import get_leetcode_profile



from database import (
    save_leetcode_username,
    get_leetcode_username
)


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

if "user_name" not in st.session_state:
    st.session_state["user_name"] = None


if not st.session_state["logged_in"]:
    st.error("Please login first.")
    st.stop()


st.title("🟧 LeetCode Dashboard")

if "user_email" in st.session_state and st.session_state["user_email"]:

    saved_username = get_leetcode_username(
        st.session_state["user_email"]
    )

else:

    saved_username = None

username = st.text_input(
    "LeetCode Username",
    value=saved_username if saved_username else ""
)


if st.button("Fetch Profile"):

    if username:

        data = get_leetcode_profile(username)

        if data and data["data"]["matchedUser"]:

            user = data["data"]["matchedUser"]

            stats = user["submitStatsGlobal"]["acSubmissionNum"]

            total_solved = stats[0]["count"]
            easy_solved = stats[1]["count"]
            medium_solved = stats[2]["count"]
            hard_solved = stats[3]["count"]

            ranking = user["profile"]["ranking"]
            reputation = user["profile"]["reputation"]

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Solved", total_solved)
            col2.metric("Easy", easy_solved)
            col3.metric("Medium", medium_solved)
            col4.metric("Hard", hard_solved)

            st.divider()

            st.metric("Ranking", ranking)
            st.metric("Reputation", reputation)

        else:
            st.error("User not found.")

if st.button("Link Account"):

    if "user_email" not in st.session_state:

        st.error("Please login first.")

    else:

        save_leetcode_username(
            st.session_state["user_email"],
            username
        )

        st.success("LeetCode account linked.")

    st.success("LeetCode account linked.")