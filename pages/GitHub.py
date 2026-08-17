import streamlit as st

from utils.github_service import (
    get_github_profile,
    get_github_repos
)

st.title("⚫ GitHub Dashboard")

username = st.text_input(
    "GitHub Username",
    placeholder="Enter GitHub username"
)

if st.button("Fetch Profile"):

    profile = get_github_profile(username)

    if profile:

        # --------------------------
        # Profile Section
        # --------------------------

        st.image(
            profile["avatar_url"],
            width=150
        )

        st.subheader(
            profile["name"]
            if profile["name"]
            else profile["login"]
        )

        st.caption(profile["login"])

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Followers",
            profile["followers"]
        )

        col2.metric(
            "Following",
            profile["following"]
        )

        col3.metric(
            "Repositories",
            profile["public_repos"]
        )

        st.divider()

        st.write(
            f"📍 Location: {profile.get('location') or 'Not Available'}"
        )

        st.write(
            f"🏢 Company: {profile.get('company') or 'Not Available'}"
        )

        st.write(
            f"📅 Joined: {profile['created_at'][:10]}"
        )

        if profile.get("bio"):
            st.info(profile["bio"])

        # --------------------------
        # Repository Section
        # --------------------------

        repos = get_github_repos(username)

        st.divider()

        st.subheader("📂 Repositories")

        for repo in repos[:10]:

            st.markdown(
                f"""
**{repo['name']}**

⭐ {repo['stargazers_count']}
| 🍴 {repo['forks_count']}
| 💻 {repo['language'] or 'Not Specified'}
"""
            )

        # --------------------------
        # Language Analysis
        # --------------------------

        languages = {}

        for repo in repos:

            lang = repo["language"]

            if lang:

                if lang not in languages:
                    languages[lang] = 0

                languages[lang] += 1

        st.divider()

        st.subheader("📊 Language Usage")

        if languages:

            for lang, count in sorted(
                languages.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.write(
                    f"💻 {lang}: {count} repositories"
                )

        else:

            st.info(
                "No programming language data available."
            )

        # --------------------------
        # Most Popular Repository
        # --------------------------

        if repos:

            top_repo = max(
                repos,
                key=lambda x: x["stargazers_count"]
            )

            st.divider()

            st.subheader(
                "🏆 Most Popular Repository"
            )

            st.write(
                f"**Repository:** {top_repo['name']}"
            )

            st.write(
                f"⭐ Stars: {top_repo['stargazers_count']}"
            )

            st.markdown(
                f"[🔗 Open Repository]({top_repo['html_url']})"
            )

    else:

        st.error(
            "GitHub user not found."
        )