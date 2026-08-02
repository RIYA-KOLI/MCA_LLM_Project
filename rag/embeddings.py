import os
from dotenv import load_dotenv
from google import genai
from config import EMBEDDING_MODEL

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_embedding(text):
    """
    Generate embedding for a single chunk of text.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values