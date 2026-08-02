import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "data/faiss_index.index"
METADATA_PATH = "data/metadata.pkl"

dimension = 3072

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

        index = faiss.read_index(INDEX_PATH)

    if os.path.exists(METADATA_PATH):

        with open(METADATA_PATH, "rb") as f:

            metadata = pickle.load(f)


def add_embeddings(chunks, embeddings):

    vectors = np.array(embeddings).astype("float32")

    index.add(vectors)

    metadata.extend(chunks)

    save_index()


def search(query_embedding, k=5):

    query = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query, k)

    results = []

    for idx in indices[0]:

        if idx < len(metadata):

            results.append(metadata[idx])

    return results