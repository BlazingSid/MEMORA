# 🧠 MEMORA

> A native desktop AI memory assistant that learns from you and helps
> you remember what you've learned, built, and discovered.

MEMORA is a local-first personal memory system built as a native Windows
desktop application. Instead of being another web chatbot, MEMORA lives
on your PC and turns your saved thoughts and experiences into a
searchable personal knowledge base.

## ✨ Current Features

-   🧠 Save personal memories and notes
-   💾 Persistent SQLite memory storage
-   🔎 Semantic search using vector embeddings
-   📚 ChromaDB vector database
-   🤖 Local Qwen 2.5 7B LLM through Ollama
-   🔗 RAG-based question answering
-   ⚡ Background LLM processing so the UI stays responsive
-   🖥️ Native PySide6 desktop interface
-   🎨 Modern dashboard-style UI
-   🕐 Local system timestamps
-   🔍 Search memories by meaning rather than exact keywords

## 🏗️ Architecture

``` text
                    ┌────────────────────┐
                    │    MEMORA Desktop  │
                    │      PySide6       │
                    └─────────┬──────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
           Save Memory                Ask MEMORA
                 │                         │
                 ▼                         ▼
              SQLite                  Semantic Search
                 │                         │
                 │                      ChromaDB
                 │                         │
                 └────────────┬────────────┘
                              ▼
                             RAG
                              │
                              ▼
                       Qwen 2.5 7B
                         via Ollama
                              │
                              ▼
                           Answer
```

## 🛠️ Tech Stack

  Layer             Technology
  ----------------- -----------------------
  Desktop UI        PySide6
  Language          Python 3.12
  Database          SQLite
  Vector Database   ChromaDB
  Embeddings        Sentence Transformers
  LLM               Qwen 2.5 7B
  Local Runtime     Ollama
  Retrieval         Semantic Search + RAG

## 📁 Project Structure

``` text
MEMORA/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── llm.py
│   │   ├── rag.py
│   │   └── llm_worker.py
│   ├── database/
│   │   ├── memory_db.py
│   │   └── vector_memory.py
│   ├── styles/
│   │   ├── colors.py
│   │   ├── fonts.py
│   │   └── theme.qss
│   └── ui/
│       ├── main_window.py
│       ├── home.py
│       ├── memories.py
│       ├── search.py
│       └── settings.py
│
├── data/
├── .venv/
└── README.md
```

## 🚀 Running MEMORA

### 1. Create and activate the virtual environment

``` bash
python -m venv .venv
```

Windows:

``` bash
.venv\Scriptsctivate
```

### 2. Install dependencies

``` bash
pip install PySide6 chromadb sentence-transformers
```

Install any additional project dependencies used by the current backend.

### 3. Make sure Ollama is running

Check:

``` bash
ollama --version
```

Then verify the model exists:

``` bash
ollama list
```

MEMORA currently uses:

``` text
qwen2.5:7b
```

If needed:

``` bash
ollama pull qwen2.5:7b
```

### 4. Start MEMORA

From the project root:

``` bash
python -m app.main
```

## 🎯 Vision

MEMORA is being built toward a true **personal second brain for the
desktop**.

The long-term goal is for MEMORA to remember useful context from your
digital life, retrieve it intelligently, and make that information
available through a fast, private local AI assistant.

Future directions include:

-   Streaming AI responses
-   Rich memory cards
-   Memory timeline
-   Topics and automatic organization
-   Better contextual retrieval
-   Global hotkey / quick access
-   System tray integration
-   Background memory capture
-   Smarter personal insights
-   Fully polished native desktop experience

## 🔐 Local-First Philosophy

MEMORA is designed around the idea that your personal memories should
stay on your machine whenever possible.

Your memories are stored locally, semantic retrieval runs locally, and
the current LLM is served locally through Ollama.

## 📌 Status

**Active development --- early prototype**

Current milestone:

``` text
Native Desktop App       ✅
SQLite Memory            ✅
Vector Memory            ✅
Semantic Search          ✅
Local Qwen LLM           ✅
RAG                      ✅
Background Processing    ✅
Modern UI                🚧
Streaming Responses      🔜
Advanced Memory System   🔜
```

------------------------------------------------------------------------

Built with Python, PySide6, ChromaDB, Ollama, and a ridiculous amount of
caffeine. ☕🧠
