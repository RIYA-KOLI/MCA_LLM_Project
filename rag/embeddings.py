from sentence_transformers import SentenceTransformer
import streamlit as st


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_embedding_model()


def generate_embedding(text):
    """
    Generate embedding for a single query.
    """

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()


def generate_embeddings(chunks):
    """
    Generate embeddings for document chunks.
    """

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings.tolist()