from app.database.vector_memory import add_memory, search_memories


add_memory(
    1001,
    "I learned how PySide6 layouts work."
)

add_memory(
    1002,
    "I started building a desktop application with Python."
)

add_memory(
    1003,
    "I learned how SQLite stores persistent data."
)


results = search_memories(
    "What did I learn about building desktop software?"
)


print("\nSemantic search results:\n")

for document in results["documents"][0]:
    print("-", document)