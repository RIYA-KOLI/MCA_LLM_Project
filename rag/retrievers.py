from rag.embeddings import generate_embedding
from rag.vectorstore import search


def retrieve_context(query, top_k=10):

    query_embedding = generate_embedding(query)

    if query_embedding is None:
        return []

    return search(query_embedding, k=top_k)