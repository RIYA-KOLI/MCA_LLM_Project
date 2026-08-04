from rag.retrievers import retrieve_context
from rag.llm import generate_response


MAX_CONTEXT_CHARS = 4000


def ask_ai(question):

    # Retrieve fewer, more relevant chunks
    chunks = retrieve_context(
        question,
        top_k=4
    )

    if not chunks:
        return (
            "I could not find that information in the uploaded documents.",
            []
        )

    context_parts = []
    current_length = 0

    for chunk in chunks:

        text = chunk["text"].strip()

        if current_length + len(text) > MAX_CONTEXT_CHARS:
            break

        context_parts.append(text)
        current_length += len(text)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an expert Programming Tutor.

STRICT RULES:

1. Answer ONLY using the provided context.
2. Never use outside knowledge.
3. If the answer is not found, reply exactly:
I could not find that information in the uploaded documents.
4. If the context contains code:
   - Return ONE markdown code block.
   - After the code block, explain it briefly.
5. Keep answers concise.

====================
CONTEXT
====================

{context}

====================
QUESTION
====================

{question}
"""

    answer = generate_response(prompt)

    return answer, chunks