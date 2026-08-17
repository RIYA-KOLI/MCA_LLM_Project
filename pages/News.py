import streamlit as st
from utils.hackernews_service import get_top_stories

# ------------------------------------------------
# PAGE HEADER
# ------------------------------------------------

st.title("📰 Developer News Hub")

st.caption(
    "Stay updated with the latest AI, Programming, Cybersecurity and Open Source news."
)

# ------------------------------------------------
# TOP BAR
# ------------------------------------------------

col1, col2 = st.columns([3, 1])

with col1:

    search_term = st.text_input(
        "🔍 Search News",
        placeholder="AI, Python, Cybersecurity..."
    )

    search_clicked = st.button("🔎 Search")

with col2:

    if st.button("🔄 Refresh"):
        st.rerun()

# ------------------------------------------------
# CATEGORY FILTER
# ------------------------------------------------

category = st.selectbox(
    "📂 Category",
    [
        "All",
        "AI",
        "Programming",
        "Cybersecurity",
        "Open Source"
    ]
)

# ------------------------------------------------
# FETCH STORIES
# ------------------------------------------------

stories = get_top_stories()

if search_clicked:
    st.toast("Searching news...")

# ------------------------------------------------
# FILTER LOGIC
# ------------------------------------------------

if category != "All":

    keywords = {
        "AI": [
            "ai",
            "openai",
            "llm",
            "chatgpt",
            "gemini",
            "anthropic"
        ],

        "Programming": [
            "python",
            "java",
            "javascript",
            "coding",
            "developer",
            "programming"
        ],

        "Cybersecurity": [
            "security",
            "hack",
            "malware",
            "cyber",
            "vulnerability"
        ],

        "Open Source": [
            "linux",
            "github",
            "open source",
            "opensource"
        ]
    }

    filtered = []

    for story in stories:

        title = story.get(
            "title",
            ""
        ).lower()

        if any(
            word in title
            for word in keywords[category]
        ):
            filtered.append(story)

    stories = filtered

# ------------------------------------------------
# SEARCH FILTER
# ------------------------------------------------

if search_term:

    stories = [

        story

        for story in stories

        if search_term.lower()
        in story.get(
            "title",
            ""
        ).lower()
    ]

# ------------------------------------------------
# SIDEBAR STATS
# ------------------------------------------------

with st.sidebar:

    st.header("📊 News Stats")

    st.metric(
        "Stories Loaded",
        len(stories)
    )

    if stories:

        highest_score = max(
            story.get("score", 0)
            for story in stories
        )

        average_score = int(

            sum(
                story.get("score", 0)
                for story in stories
            )
            /
            len(stories)

        )

        st.metric(
            "Highest Score",
            highest_score
        )

        st.metric(
            "Average Score",
            average_score
        )

    st.divider()

    st.info(
        """
        🧠 Future Scope

        • AI News Digest

        • Personalized Feed

        • Save Articles

        • Daily Developer Newsletter
        """
    )

# ------------------------------------------------
# NO RESULTS
# ------------------------------------------------

if not stories:

    st.warning(
        "No stories found."
    )

    st.stop()

# ------------------------------------------------
# FEATURED STORY
# ------------------------------------------------

hero = stories[0]

st.markdown("---")

st.subheader("🔥 Trending Story")

st.markdown(
    f"## {hero['title']}"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "👍 Score",
        hero.get("score", 0)
    )

with col2:

    st.metric(
        "💬 Comments",
        hero.get(
            "descendants",
            0
        )
    )

if hero.get("url"):

    st.link_button(
        "📖 Read Full Story",
        hero["url"]
    )

st.markdown("---")

# ------------------------------------------------
# LATEST NEWS
# ------------------------------------------------

st.subheader("📰 Latest Headlines")

for story in stories[1:]:

    with st.container():

        st.markdown(
            f"### {story['title']}"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"👍 Score: {story.get('score', 0)}"
            )

        with c2:

            st.write(
                f"💬 Comments: {story.get('descendants', 0)}"
            )

        if story.get("url"):

            st.link_button(
                "Open Article",
                story["url"],
                key=f"story_{story['id']}"
            )

        st.markdown("---")