from rag.embeddings import generate_embedding
from rag.vectorstore import search


def retrieve_context(query, top_k=5):
    """
    Retrieve the most relevant document chunks for a query.
    """

    query_embedding = generate_embedding(query)

    results = search(query_embedding, k=top_k)

    return results