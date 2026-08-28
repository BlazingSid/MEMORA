from app.database.memory_db import save_memory, get_memories


memory_id = save_memory(
    "I started building MEMORA today."
)

print(f"Saved memory #{memory_id}")

memories = get_memories()

for memory in memories:
    print(memory)