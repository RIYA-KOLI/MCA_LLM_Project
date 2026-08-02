from rag.embeddings import generate_embedding

vector = generate_embedding(
    "Python is a high-level programming language."
)

print("Embedding Length:", len(vector))

print(vector[:10])