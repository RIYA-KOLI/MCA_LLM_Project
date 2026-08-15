import os
import re
import streamlit as st
from pathlib import Path

from auth import signup_user, login_user
from database import init_db
from rag.code_runner import run_code
from streamlit_mic_recorder import speech_to_text
from vision.caption import analyze_image
from rag.chat import ask_ai
from rag.voice import speak
from rag.processor import (
    process_uploaded_documents,
    get_knowledge_base_stats,
    get_uploaded_pdfs,
)

from components.code_card import render_code_card


# ==========================================================
# Load Custom CSS
# ==========================================================

def load_css():
    css_path = Path(__file__).parent / "assets" / "style.css"

    print("CSS Path:", css_path)
    print("Exists:", css_path.exists())

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


# ==========================================================
# Streamlit Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Programming Help Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

load_css()

init_db()

if not st.session_state.logged_in:

    st.title("🔐 Login System")

    login_tab, signup_tab = st.tabs(
        ["Login", "Signup"]
    )

    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            if login_user(
                email,
                password
            ):

                st.session_state.logged_in = True

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Invalid credentials."
                )

    with signup_tab:

        name = st.text_input(
            "Name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button("Create Account"):

            success, msg = signup_user(
                name,
                email,
                password
            )

            if success:

                st.success(msg)

            else:

                st.error(msg)

    st.stop()

# ==========================================================
# Upload Folder
# ==========================================================

UPLOAD_FOLDER = "knowledge_base/pdf/uploaded"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)

IMAGE_FOLDER = "knowledge_base/images"

os.makedirs(
    IMAGE_FOLDER,
    exist_ok=True
)


# ==========================================================
# Hero Section
# ==========================================================

st.markdown(
    """
<div class="hero-title">
🤖 Programming Help Assistant
</div>

<div class="hero-subtitle">
AI Powered Programming Tutor • PDF Knowledge Base • Vision AI • Voice Assistant
</div>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# Status Cards
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("📚", "Knowledge Base"),
    ("🎤", "Voice Ready"),
    ("🖼️", "Vision AI"),
    ("⚡", "FAISS Search"),
]

for column, (icon, title) in zip(
    [col1, col2, col3, col4],
    cards,
):
    with column:
        st.markdown(
            f"""
<div class="status-card">
    <div class="status-number">{icon}</div>
    <div class="status-text">{title}</div>
</div>
""",
            unsafe_allow_html=True,
        )

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("📂 Document Management")

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()

uploaded_files = st.sidebar.file_uploader(
    "Upload Programming PDFs",
    type=["pdf"],
    accept_multiple_files=True,
)

uploaded_image = st.sidebar.file_uploader(
    "🖼 Upload Code Screenshot",
    type=["png", "jpg", "jpeg"],
)

analyze_image_btn = st.sidebar.button(
    "🧠 Analyze Image",
    use_container_width=True
)

process_documents = st.sidebar.button(
    "⚙️ Process Documents",
    use_container_width=True,
)

# ==========================================================
# Process Uploaded PDFs
# ==========================================================

if process_documents:

    if not uploaded_files:

        st.sidebar.warning(
            "Please upload at least one PDF."
        )

    else:

        with st.spinner("📚 Processing Documents..."):

            for file in uploaded_files:

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.name,
                )

                with open(save_path, "wb") as f:

                    f.write(file.getbuffer())

            success, message = process_uploaded_documents(
                UPLOAD_FOLDER
            )

        if success:

            st.sidebar.success(message)

            st.rerun()

        else:

            st.sidebar.error(message)


# ==========================================
# Vision AI
# ==========================================

if analyze_image_btn:

    if uploaded_image is None:

        st.sidebar.warning(
            "Please upload an image first."
        )

    else:

        image_path = os.path.join(
            IMAGE_FOLDER,
            uploaded_image.name
        )

        with open(image_path, "wb") as f:

            f.write(uploaded_image.getbuffer())

        with st.spinner("🧠 Analyzing image..."):

            vision_result = analyze_image(image_path)

            try:
                os.remove(image_path)
            except:
                pass

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"🖼 **Vision AI Analysis**\n\n{vision_result}"
            }
        )

        st.rerun()

        
# ==========================================================
# Knowledge Base Statistics
# ==========================================================

stats = get_knowledge_base_stats(
    UPLOAD_FOLDER
)

st.sidebar.divider()

st.sidebar.subheader(
    "📊 Knowledge Base Statistics"
)

metric1, metric2 = st.sidebar.columns(2)

with metric1:

    st.metric(
        "PDFs",
        stats["pdfs"]
    )

    st.metric(
        "Chunks",
        stats["chunks"]
    )

with metric2:

    st.metric(
        "Pages",
        stats["pages"]
    )

    st.metric(
        "Indexed",
        stats["indexed_files"]
    )

# ==========================================================
# Knowledge Base Explorer
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📚 Knowledge Base"
)

pdf_list = get_uploaded_pdfs(
    UPLOAD_FOLDER
)

if not pdf_list:

    st.sidebar.info(
        "No PDFs uploaded yet."
    )

else:

    for pdf in pdf_list:

        with st.sidebar.expander(
            f"📘 {pdf['name']}"
        ):

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Pages",
                    pdf["pages"]
                )

            with c2:

                st.metric(
                    "Status",
                    "✅"
                )

            st.caption(
                "Indexed in Knowledge Base"
            )

# ==========================================================
# Chat Section
# ==========================================================

st.write(
    "Ask questions about your uploaded programming documents."
)

# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ==========================================================
# Render Chat History
# ==========================================================

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        # --------------------------------------
        # USER MESSAGE
        # --------------------------------------

        if message["role"] == "user":

            st.markdown(
                message["content"]
            )

            continue

        # --------------------------------------
        # ASSISTANT MESSAGE
        # --------------------------------------

        st.markdown(
            message["content"]
        )

        # --------------------------------------
        # Code Card
        # --------------------------------------

        if message.get("code"):

            edit_clicked, copy_clicked = render_code_card(

                code=message["code"],

                language=message["language"],

                message_id=index,

            )

            if copy_clicked:

                st.toast(
                    "Copy feature coming soon."
                )

            if edit_clicked:
                st.session_state[f"editing_{index}"] = True

            if st.session_state.get(f"editing_{index}", False):

                edited_code = st.text_area(
                    "Edit Code",
                    value=message["code"],
                    height=300,
                    key=f"editor_{index}"
                )
                if st.button(
                    "Run Edited Code",
                    key=f"run_edited_btn_{index}"
                ):
                    st.success("BUTTON CLICKED")

                    st.write("DEBUG CODE:")
                    st.code(edited_code)

                    output = run_code(
                        edited_code,
                        message["language"]
                    )

                    st.markdown("### Output")
                    st.code(output)



        # --------------------------------------
        # Sources
        # --------------------------------------

        sources = message.get(
            "sources",
            []
        )

        st.divider()

        if sources:

            st.markdown(
                "#### 📄 Sources"
            )

            displayed = set()

            chips = ""

            for source in sources:

                key = (

                    source["file_name"],

                    source["page_number"]

                )

                if key in displayed:

                    continue

                displayed.add(key)

                score = source.get(
                    "score",
                    0
                )

                chips += f"""
                <span class="source-chip">
                📘 {source['file_name']}
                • Pg {source['page_number']}
                • ⭐ {score:.1f}%
                </span>
                """

            st.markdown(

                chips,

                unsafe_allow_html=True

            )

        else:

            st.info(
                "No sources available."
            )

# ---------------------------------------
# Play generated speech
# ---------------------------------------

if "audio_path" in st.session_state:

    with open(st.session_state.audio_path, "rb") as audio:

        st.audio(
            audio.read(),
            format="audio/mp3",
            autoplay=True,
        )

    del st.session_state.audio_path

# ==========================================================
# Voice Input
# ==========================================================

voice_text = speech_to_text(

    language="en",

    start_prompt="🎤 Speak",

    stop_prompt="⏹ Stop",

    use_container_width=True,

    just_once=True,

    key="voice_input"

)

question = st.chat_input(

    "Ask a programming question..."

)

if not question and voice_text:

    question = voice_text

if voice_text:

    st.success(
        f"🎤 You said: {voice_text}"
    )

# ==========================================================
# Process New Question
# ==========================================================

if question:

    # -----------------------------
    # Save User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # -----------------------------
    # Generate Answer
    # -----------------------------

    try:

        answer, sources = ask_ai(question)

    except Exception as e:

        answer = f"⚠️ Error\n\n{e}"

        sources = []

    # -----------------------------
    # Extract Code
    # -----------------------------

    code = None
    language = None
    display_answer = answer

    match = re.search(
        r"```(\w+)\n(.*?)```",
        answer,
        re.DOTALL,
    )

    if match:

        language = match.group(1)

        code = match.group(2).strip()

        # Remove code block from assistant text
        display_answer = re.sub(
            r"```.*?```",
            "",
            answer,
            flags=re.DOTALL
        ).strip()

    # -----------------------------
    # Save Assistant Message
    # -----------------------------

    assistant_message = {

        "role": "assistant",

        "content": display_answer,

        "sources": sources,

        "code": code,

        "language": language,

    }

    st.session_state.messages.append(
        assistant_message
    )

    # -----------------------------
    # Voice Output
    # -----------------------------

    if voice_text:

        st.write("Generating audio...")

        st.session_state.audio_path = speak(display_answer)

        st.write(st.session_state.audio_path)

    # -----------------------------
    # Refresh UI
    # -----------------------------

    st.rerun()
    