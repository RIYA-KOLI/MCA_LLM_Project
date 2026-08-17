# pages/Developer_Intelligence.py

import streamlit as st
import pandas as pd

from utils.github_service import (
    get_github_profile,
    get_github_repos
)

from utils.leetcode_service import (
    get_leetcode_profile
)

from rag.llm import generate_response


st.title("📊 Developer Intelligence")

st.caption(
    "AI-powered analysis using GitHub + LeetCode + Qwen"
)

github_username = st.text_input(
    "GitHub Username"
)

leetcode_username = st.text_input(
    "LeetCode Username"
)

if st.button("🚀 Generate AI Report"):

    if not github_username or not leetcode_username:

        st.warning(
            "Please enter both usernames."
        )

        st.stop()

    # ---------------------------
    # GitHub Data
    # ---------------------------

    github_profile = get_github_profile(
        github_username
    )

    repos = get_github_repos(
        github_username
    )

    if not github_profile:

        st.error(
            "Invalid GitHub username."
        )

        st.stop()

    followers = github_profile["followers"]

    public_repos = github_profile["public_repos"]

    # language analysis

    languages = {}

    for repo in repos:

        lang = repo.get("language")

        if lang:

            if lang not in languages:
                languages[lang] = 0

            languages[lang] += 1

    top_languages = sorted(
        languages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_languages = [
        lang[0]
        for lang in top_languages[:5]
    ]

    # ---------------------------
    # LeetCode Data
    # ---------------------------

    lc_data = get_leetcode_profile(
        leetcode_username
    )

    if not lc_data["data"]["matchedUser"]:

        st.error(
            "Invalid LeetCode username."
        )

        st.stop()

    user = lc_data["data"]["matchedUser"]

    stats = user["submitStatsGlobal"]["acSubmissionNum"]

    total_solved = stats[0]["count"]
    easy_solved = stats[1]["count"]
    medium_solved = stats[2]["count"]
    hard_solved = stats[3]["count"]

    ranking = user["profile"]["ranking"]

    # ---------------------------
    # Data Fusion
    # ---------------------------

    developer_profile = {

        "GitHub Username":
        github_username,

        "Followers":
        followers,

        "Repositories":
        public_repos,

        "Languages":
        ", ".join(top_languages),

        "LeetCode Username":
        leetcode_username,

        "Problems Solved":
        total_solved,

        "Easy":
        easy_solved,

        "Medium":
        medium_solved,

        "Hard":
        hard_solved,

        "Ranking":
        ranking
    }

    st.success(
        "Data Fusion Completed"
    )

    st.json(
        developer_profile
    )

    # ---------------------------
    # AI Analysis
    # ---------------------------

    prompt = f"""
    Analyze this developer profile.

    GitHub:
    Followers: {followers}
    Repositories: {public_repos}
    Languages: {', '.join(top_languages)}

    LeetCode:
    Total Solved: {total_solved}
    Easy: {easy_solved}
    Medium: {medium_solved}
    Hard: {hard_solved}
    Ranking: {ranking}

    Provide:

    1. Skill Assessment

    2. Strengths

    3. Weaknesses

    4. Learning Roadmap

    5. Suggested Projects

    Keep the response concise.
    """

    with st.spinner(
        "Generating AI report..."
    ):

        report = generate_response(
            prompt
        )

    st.subheader(
        "🤖 AI Career Report"
    )

    st.write(
        report
    )

    # ---------------------------
    # Excel Export
    # ---------------------------

    df = pd.DataFrame(
        [developer_profile]
    )

    file_name = (
        "developer_report.xlsx"
    )

    df.to_excel(
        file_name,
        index=False
    )

    with open(
        file_name,
        "rb"
    ) as f:

        st.download_button(
            label="📥 Download Excel Report",
            data=f,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )