# RAG PDF Chatbot

Question-answering chatbot over PDF documents using OpenAI embeddings and ChromaDB.

## ⚠️ Python Version

Requires **Python 3.12 or earlier** — ChromaDB is not compatible with Python 3.13.

## Patterns

- PDF ingestion: extract → chunk (400 words, 80 overlap) → embed → store in ChromaDB
- Query: embed question → semantic search → retrieve top chunks → GPT-4o-mini answer
- `connector_instances=None` — lazy OpenAI connector initialization

## Setup

```bash
pip install pdfplumber chromadb openai
```

Requires `OPENAI_API_KEY` in Secrets connector or environment.

## Endpoints

- `POST /ingest` — upload and ingest PDF (multipart form, field: `file`)
- `POST /query` — ask a question (`{"question": "..."}`)
