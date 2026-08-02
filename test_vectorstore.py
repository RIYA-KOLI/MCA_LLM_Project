from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.embeddings import generate_embedding
from rag.vectorstore import add_embeddings

print("Loading PDFs...")
docs = load_documents()

print("Chunking...")
chunks = chunk_documents(docs)

chunks = chunks[:5]

print("Generating embeddings...")

embeddings = []

for chunk in chunks:

    embeddings.append(generate_embedding(chunk["text"]))

print("Saving into FAISS...")

add_embeddings(chunks, embeddings)

print("SUCCESS")

from rag.retrievers import retrieve_context

print("\nTesting Retriever...\n")

results = retrieve_context("What is Python?")

for i, chunk in enumerate(results, 1):
    print("=" * 60)
    print(f"Result {i}")
    print("=" * 60)
    print(chunk["text"][:400])