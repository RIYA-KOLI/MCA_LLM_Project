from rag.chat import ask_ai

question = input("Ask a Question: ")

answer, sources = ask_ai(question)

print("\n")
print("=" * 80)
print("AI ANSWER")
print("=" * 80)

print(answer)

print("\n")
print("=" * 80)
print("SOURCES")
print("=" * 80)

for source in sources:

    print(source["file_name"])

    print("Page:", source["page_number"])

    print()