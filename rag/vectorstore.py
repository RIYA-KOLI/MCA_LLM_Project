import os
import pickle

import faiss
import numpy as np
import streamlit as st

INDEX_PATH = "data/faiss_index.index"
METADATA_PATH = "data/metadata.pkl"

DIMENSION = 384


# ==========================================================
# Load FAISS Once
# ==========================================================

@st.cache_resource
def load_vector_store():

    index = faiss.IndexFlatL2(DIMENSION)
    metadata = []

    if os.path.exists(INDEX_PATH):

        index = faiss.read_index(INDEX_PATH)

    if os.path.exists(METADATA_PATH):

        with open(METADATA_PATH, "rb") as f:

            metadata = pickle.load(f)

    return index, metadata


index, metadata = load_vector_store()


# ==========================================================
# Save
# ==========================================================

def save_index():

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(METADATA_PATH, "wb") as f:

        pickle.dump(
            metadata,
            f
        )


# ==========================================================
# Add New Embeddings
# ==========================================================

def add_embeddings(chunks, embeddings):

    vectors = np.asarray(
        embeddings,
        dtype=np.float32
    )

    index.add(vectors)

    metadata.extend(chunks)

    save_index()

    # Refresh cache after modifying the index
    load_vector_store.clear()


# ==========================================================
# Search
# ==========================================================

def search(query_embedding, k=5):

    if not metadata:

        return []

    query = np.asarray(
        [query_embedding],
        dtype=np.float32
    )

    distances, indices = index.search(
        query,
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx < 0 or idx >= len(metadata):

            continue

        result = metadata[idx].copy()

        similarity = 100 / (1 + float(distance))

        result["score"] = round(
            similarity,
            2
        )

        if similarity >= 20:

            results.append(result)

    return results