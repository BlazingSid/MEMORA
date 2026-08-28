import time

from app.database.vector_memory import search_memories
from app.core.llm import generate_response


def ask_memora(question: str, n_results: int = 3) -> str:

    start = time.time()

    results = search_memories(
        question,
        n_results=n_results,
    )

    retrieval_time = time.time() - start

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "I couldn't find any relevant memories about that yet."

    memory_context = "\n".join(
        f"- {memory}"
        for memory in documents
    )

    prompt = f"""
You are MEMORA, a personal AI memory assistant.

Answer the user's question using ONLY the memories
provided below.

If the memories do not contain enough information,
say that you don't know instead of inventing details.

Relevant memories:

{memory_context}

User question:

{question}

Answer naturally and concisely.
"""

    llm_start = time.time()

    answer = generate_response(prompt)

    llm_time = time.time() - llm_start

    print(f"\nRetrieval: {retrieval_time:.2f}s")
    print(f"LLM:       {llm_time:.2f}s")
    print(f"Total:     {retrieval_time + llm_time:.2f}s")

    return answer