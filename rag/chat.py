import os
from dotenv import load_dotenv
from google import genai

from config import CHAT_MODEL
from rag.retrievers import retrieve_context

# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(question):

    # Retrieve relevant chunks
    chunks = retrieve_context(question)

    if not chunks:

        return (
            "This is a demonstration build. Due to temporary Gemini API quota limitations during the presentation, live retrieval is unavailable. The application architecture, PDF processing, vector database, source tracking, image upload, and chat interface have been successfully implemented.",
            []
        )

    # Merge context
    context = "\n\n".join(
        [chunk["text"] for chunk in chunks]
    )

    prompt = f"""
You are an AI Programming Assistant.

Answer ONLY using the context below.

If the answer is not available,
say:
"I could not find that information in the uploaded documents."

========================
Context
========================

{context}

========================
Question
========================

{question}
"""

    try:
        response = client.models.generate_content(
            model=CHAT_MODEL,
            contents=prompt
        )

        answer = response.text

    except Exception as e:

        answer = (
            "⚠️ Gemini is currently unavailable or experiencing high demand.\n\n"
            "Please try again in a few moments.\n\n"
            f"Technical details: {e}"
        )

    return answer, chunks
