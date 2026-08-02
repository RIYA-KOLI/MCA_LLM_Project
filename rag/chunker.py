def chunk_documents(documents, chunk_size=1000, overlap=200):
    """
    Split documents into overlapping text chunks.
    """

    chunks = []

    for doc in documents:

        text = doc["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            if chunk.strip():

                chunks.append({

                    "file_name": doc["file_name"],

                    "page_number": doc["page_number"],

                    "text": chunk

                })

            start += chunk_size - overlap

    return chunks