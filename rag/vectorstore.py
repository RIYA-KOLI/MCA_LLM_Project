import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "data/faiss_index.index"
METADATA_PATH = "data/metadata.pkl"

dimension = 384

index = faiss.IndexFlatL2(dimension)

metadata = []


def save_index():
    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    global index
    global metadata

    if os.path.exists(INDEX_PATH):
        print("Loading FAISS index...")
        index = faiss.read_index(INDEX_PATH)

    if os.path.exists(METADATA_PATH):
        print("Loading metadata...")

        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)

    print("Loaded vectors:", index.ntotal)
    print("Loaded metadata:", len(metadata))


def add_embeddings(chunks, embeddings):

    vectors = np.array(embeddings).astype("float32")

    index.add(vectors)

    metadata.extend(chunks)

    save_index()


def search(query_embedding, k=10):

    print("Metadata length:", len(metadata))

    if query_embedding is None:
        return []

    # If metadata is empty, return nothing
    if len(metadata) == 0:
        return []

    query = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        # Skip invalid FAISS results
        if idx == -1:
            continue

        # Skip out-of-range indices
        if idx >= len(metadata):
            continue

        result = metadata[idx].copy()

        distance = float(distance)

        similarity = 100 / (1 + distance)

        result["score"] = round(similarity, 2)

        if similarity >= 20:
            results.append(result)

    return results

# -----------------------------------
# Automatically load saved FAISS index
# -----------------------------------

load_index()