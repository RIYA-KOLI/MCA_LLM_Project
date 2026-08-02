import streamlit as st
import os

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="CodeAssist AI",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Header
# ----------------------------
st.title("🤖 CodeAssist AI")
st.caption("RAG-Based Programming Learning Assistant")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("📂 Document Management")

uploaded_files = st.file_uploader(
    "Upload Programming PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} file(s) selected")

    for file in uploaded_files:
        st.write("📄", file.name)

    if st.button("📚 Process Documents"):

        os.makedirs("data", exist_ok=True)

        for file in uploaded_files:

            save_path = os.path.join("data", file.name)

            with open(save_path, "wb") as f:
                f.write(file.getbuffer())

        st.success("Documents uploaded successfully!")

    st.divider()

    st.header("⚙️ AI Mode")

    mode = st.selectbox(
        "Choose Mode",
        [
            "General Programming",
            "Assignment Hints",
            "Debug Assistant",
            "Complexity Analyzer",
            "Code Review",
            "Concept Explainer",
            "Teacher Feedback"
        ]
    )

# ----------------------------
# Chat Section
# ----------------------------
st.subheader("💬 Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your programming question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = (
        "🚧 AI integration coming next.\n\n"
        f"Current Mode: **{mode}**"
    )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# ----------------------------
# Source Documents
# ----------------------------
st.divider()

st.subheader("📖 Source Documents")

st.info("Relevant document chunks will appear here after RAG is implemented.")