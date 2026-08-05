import os
import json
import pickle
import fitz

from rag.loader import load_uploaded_documents
from rag.chunker import chunk_documents
from rag.embeddings import generate_embeddings
from rag.vectorstore import add_embeddings

INDEXED_FILE = "data/indexed_files.json"


def _load_indexed_files():

    if not os.path.exists(INDEXED_FILE):
        return []

    with open(INDEXED_FILE, "r") as f:
        return json.load(f)


def _save_indexed_files(files):

    #print("Writing to:", os.path.abspath(INDEXED_FILE))

    with open(INDEXED_FILE, "w") as f:
        json.dump(files, f, indent=4)


def process_uploaded_documents(upload_folder):

    indexed_files = _load_indexed_files()

    pdfs_to_process = []

    for file in os.listdir(upload_folder):

        if file.lower().endswith(".pdf") and file not in indexed_files:

            pdfs_to_process.append(file)

    if not pdfs_to_process:

        return True, "No new PDFs found."

    try:

        documents = load_uploaded_documents(
            upload_folder,
            pdfs_to_process
        )

        print(documents[:5])

        chunks = chunk_documents(documents)

        print("Chunks created:", len(chunks))

        embeddings = generate_embeddings(chunks)
        print("Embeddings generated:", len(embeddings))

        add_embeddings(chunks, embeddings)
        print("Chunks:", len(chunks))

        print("FAISS vectors:", len(embeddings))

        print("Saved to FAISS successfully!")

        print("FAISS Saved Successfully")

        indexed_files.extend(pdfs_to_process)
        #print("Indexed Files:", indexed_files)

        _save_indexed_files(indexed_files)
        #print("Saved indexed_files.json")

        return True, f"{len(pdfs_to_process)} PDF(s) processed successfully."

        import traceback

    except Exception as e:

        traceback.print_exc()

        return False, str(e)

def get_knowledge_base_stats(upload_folder):
    """
    Returns statistics about the knowledge base.
    """

    stats = {
        "pdfs": 0,
        "pages": 0,
        "chunks": 0,
        "indexed_files": 0
    }

    # Count PDFs
    pdf_files = [
        f for f in os.listdir(upload_folder)
        if f.lower().endswith(".pdf")
    ]

    stats["pdfs"] = len(pdf_files)

    # Count indexed files
    indexed = _load_indexed_files()
    stats["indexed_files"] = len(indexed)

    # Count pages
    for pdf_name in pdf_files:

        with fitz.open(
            os.path.join(upload_folder, pdf_name)
        ) as pdf:

            stats["pages"] += len(pdf)

    # Count chunks
    if os.path.exists("data/metadata.pkl"):

        with open("data/metadata.pkl", "rb") as f:

            metadata = pickle.load(f)

            stats["chunks"] = len(metadata)

    return stats

def get_uploaded_pdfs(upload_folder):
    """
    Returns a list of uploaded PDFs with their page count.
    """

    pdf_list = []

    for file in os.listdir(upload_folder):

        if file.lower().endswith(".pdf"):

            pdf_path = os.path.join(upload_folder, file)

            with fitz.open(pdf_path) as pdf:

                pdf_list.append(
                    {
                        "name": file,
                        "pages": len(pdf)
                    }
                )

    return sorted(
        pdf_list,
        key=lambda x: x["name"].lower()
    )