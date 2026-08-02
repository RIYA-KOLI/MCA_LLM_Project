from rag.loader import load_documents
from rag.chunker import chunk_documents

documents = load_documents()

chunks = chunk_documents(documents)

print("=" * 60)

print(f"Documents Loaded : {len(documents)}")

print(f"Chunks Created   : {len(chunks)}")

print("=" * 60)

print("\nSample Chunk:\n")

print(chunks[0]["text"][:1000])