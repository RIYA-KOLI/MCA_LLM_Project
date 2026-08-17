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
            f"📍 Location: {profile.get('location', 'Not Available')}"
        )

        st.write(
            f"🏢 Company: {profile.get('company', 'Not Available')}"
        )

        st.write(
            f"📅 Joined: {profile['created_at'][:10]}"
        )

        if profile.get("bio"):
            st.info(profile["bio"])

        # --------------------------
        # Repositories
        # --------------------------

        repos = get_github_repos(username)

        st.subheader("📂 Repositories")

        for repo in repos[:10]:

            st.markdown(
                f"""
                **{repo['name']}**

                ⭐ {repo['stargazers_count']}
                | 🍴 {repo['forks_count']}
                | 💻 {repo['language']}
                """
            )

    else:
        st.error("GitHub user not found.")