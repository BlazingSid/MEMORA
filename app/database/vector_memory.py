from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "data" / "chroma"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="memora_memories"
)


def add_memory(memory_id: int, content: str):
    embedding = model.encode(content).tolist()

    collection.add(
        ids=[str(memory_id)],
        documents=[content],
        embeddings=[embedding],
    )


def search_memories(query: str, n_results: int = 3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results

def search_memory_documents(
    query: str,
    n_results: int = 10,
):
    results = search_memories(
        query,
        n_results=n_results,
    )

    return results.get(
        "documents",
        [[]]
    )[0]