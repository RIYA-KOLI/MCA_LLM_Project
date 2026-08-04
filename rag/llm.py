import streamlit as st
import ollama

MODEL_NAME = "qwen2.5:3b"


@st.cache_resource
def get_ollama_client():
    """
    Create the Ollama client only once.
    """
    return ollama


client = get_ollama_client()


def generate_response(prompt):
    """
    Send a prompt to the local Qwen model.
    """

    try:

        response = client.chat(

            model=MODEL_NAME,

            keep_alive=-1,

            options={
                "temperature": 0.2,
                "num_predict": 512,
            },

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"⚠️ Local LLM Error:\n\n{e}"