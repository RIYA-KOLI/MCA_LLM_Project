import os
import streamlit as st

from rag.voice import speak
from streamlit_mic_recorder import speech_to_text
from rag.chat import ask_ai
from rag.vision import analyze_code_image
from rag.processor import (
    process_uploaded_documents,
    get_knowledge_base_stats,
    get_uploaded_pdfs
)

def load_css():

    with open("assets/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True

        )

# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="Programming Help Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

st.markdown("""

<div class="hero-title">

🤖 Programming Help Assistant

</div>

<div class="hero-subtitle">

AI Powered Programming Tutor • PDF Knowledge Base • Vision AI • Voice Assistant

</div>

""",

unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown("""

<div class="status-card">

<div class="status-number">📚</div>

<div class="status-text">

Knowledge Base

</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown("""

<div class="status-card">

<div class="status-number">🎤</div>

<div class="status-text">

Voice Ready

</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown("""

<div class="status-card">

<div class="status-number">🖼</div>

<div class="status-text">

Vision AI

</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown("""

<div class="status-card">

<div class="status-number">⚡</div>

<div class="status-text">

FAISS Search

</div>

</div>

""",unsafe_allow_html=True)

# ==========================================
# Upload Folder
# ==========================================

UPLOAD_FOLDER = "knowledge_base/pdf/uploaded"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("📂 Document Management")

uploaded_files = st.sidebar.file_uploader(
    "Upload Programming PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

uploaded_image = st.sidebar.file_uploader(
    "🖼 Upload Code Screenshot",
    type=["png", "jpg", "jpeg"]
)

process = st.sidebar.button(
    "⚙️ Process Documents"
)

# ==========================================
# Knowledge Base Statistics
# ==========================================

stats = get_knowledge_base_stats(
    UPLOAD_FOLDER
)

st.sidebar.divider()

st.sidebar.subheader(
    "📊 Knowledge Base Statistics"
)

col1, col2 = st.sidebar.columns(2)

with col1:

    st.metric(
        "PDFs",
        stats["pdfs"]
    )

    st.metric(
        "Chunks",
        stats["chunks"]
    )

with col2:

    st.metric(
        "Pages",
        stats["pages"]
    )

    st.metric(
        "Indexed",
        stats["indexed_files"]
    )

# ==========================================
# Knowledge Base Explorer
# ==========================================

st.sidebar.divider()

st.sidebar.subheader(
    "📚 Knowledge Base"
)

pdfs = get_uploaded_pdfs(
    UPLOAD_FOLDER
)

if pdfs:

    for pdf in pdfs:

        with st.sidebar.expander(
            f"📘 {pdf['name']}"
        ):

            col1, col2 = st.columns(2)

            col1.metric(
                "Pages",
                pdf["pages"]
            )

            col2.metric(
                "Status",
                "✅"
            )

            st.caption(
                "Indexed in Knowledge Base"
            )

else:

    st.sidebar.info(
        "No PDFs uploaded yet."
    )

# ==========================================
# Process Documents
# ==========================================

if process:

    if uploaded_files:

        with st.spinner(
            "📚 Processing Documents..."
        ):

            for file in uploaded_files:

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.name
                )

                with open(
                    save_path,
                    "wb"
                ) as f:

                    f.write(
                        file.getbuffer()
                    )

            success, message = process_uploaded_documents(
                UPLOAD_FOLDER
            )

            if success:

                st.sidebar.success(
                    message
                )

                st.rerun()

            else:

                st.sidebar.error(
                    "⚠️ " + message
                )

    else:

        st.sidebar.warning(
            "Please upload at least one PDF."
        )

# ==========================================
# Chat Section
# ==========================================

st.write(
    "Ask questions about your uploaded programming documents."
)

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# -----------------------------
# Voice Input
# -----------------------------

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

# Use voice if no text was typed
if not question and voice_text:
    question = voice_text

if voice_text:
    st.success(f"🎤 You said: {voice_text}")

if question:

    st.chat_message(
        "user"
    ).markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

# ==========================================
# Decide whether to use Image AI or PDF RAG
# ==========================================

    if uploaded_image is not None:

        image_bytes = uploaded_image.getvalue()

        answer = (
            "⚠️ Image analysis is temporarily unavailable."
        )

        sources = []

    else:

        import traceback

        try:

            answer, sources = ask_ai(question)

        except Exception as e:

            traceback.print_exc()   # <-- prints the full error in the terminal

            answer = (
                f"⚠️ Error:\n\n{e}"
            )

            sources = []

        

    with st.chat_message(
        "assistant"
    ):

        st.markdown(answer)

        # Automatically speak only when the user used voice input
        if voice_text:

            audio_path = speak(answer)

            with open(audio_path, "rb") as audio_file:

                st.audio(
                    audio_file.read(),
                    format="audio/mp3",
                    autoplay=True
                )        

        st.divider()

        if sources:

            st.markdown("#### 📄 Sources")

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

                score = source.get("score", 0)

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

    # ==========================================
    # Save Assistant Message
    # ==========================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ==========================================
# Download Conversation
# ==========================================

if st.session_state.messages:

    conversation = ""

    for message in st.session_state.messages:

        role = (
            "You"
            if message["role"] == "user"
            else "Assistant"
        )

        conversation += (
            f"{role}:\n"
            f"{message['content']}\n\n"
            + "-" * 60
            + "\n\n"
        )

    st.sidebar.divider()

    st.sidebar.download_button(

        label="⬇ Download Conversation",

        data=conversation,

        file_name="conversation.txt",

        mime="text/plain"
    )