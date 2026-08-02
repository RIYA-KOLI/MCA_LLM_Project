import os
import fitz  # PyMuPDF


def load_documents(folder_path="knowledge_base"):
    """
    Recursively load all PDF documents from the knowledge base.
    Returns a list of dictionaries containing:
    - file_name
    - page_number
    - text
    """

    documents = []

    for root, _, files in os.walk(folder_path):
        for file in files:

            if file.lower().endswith(".pdf"):

                pdf_path = os.path.join(root, file)

                pdf = fitz.open(pdf_path)

                for page_num in range(len(pdf)):

                    page = pdf.load_page(page_num)

                    text = page.get_text()

                    if text.strip():

                        documents.append({
                            "file_name": file,
                            "page_number": page_num + 1,
                            "text": text
                        })

                pdf.close()

    return documents