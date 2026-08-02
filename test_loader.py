from rag.loader import load_documents

documents = load_documents()

print("=" * 50)
print(f"Total Pages Loaded: {len(documents)}")
print("=" * 50)

for doc in documents[:10]:
    print(doc["file_name"], "| Page", doc["page_number"])