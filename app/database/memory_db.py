import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "memora.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    return connection


def save_memory(content: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO memories (content) VALUES (?)",
        (content,)
    )

    connection.commit()

    memory_id = cursor.lastrowid

    connection.close()

    return memory_id


def get_memories():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, content, created_at
        FROM memories
        ORDER BY created_at DESC
    """)

    memories = cursor.fetchall()

    connection.close()

    return memories