import streamlit as st
from rag.code_runner import run_code


def render_code_card(code, language, message_id):

    st.markdown(f"## 💻 {language.capitalize()} Code")

    st.code(
        code,
        language=language
    )

    c1, c2, c3, c4 = st.columns(4)

    run_clicked = c1.button(
        "▶ Run",
        key=f"run_{message_id}"
    )

    edit_clicked = c2.button(
        "✏ Edit",
        key=f"edit_{message_id}"
    )

    copy_clicked = c3.button(
        "📋 Copy",
        key=f"copy_{message_id}"
    )

    c4.download_button(
        "💾 Save",
        data=code,
        file_name=f"program.{language}",
        mime="text/plain",
        key=f"save_{message_id}",
    )

    # -----------------------------
    # Run Code
    # -----------------------------

    if run_clicked:

        with st.spinner("Running code..."):

            output = run_code(
                code,
                language
            )

        st.markdown("### 🖥 Output")

        st.code(
            output,
            language="text"
        )

    return edit_clicked, copy_clicked