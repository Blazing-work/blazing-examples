# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `OPENAI_API_KEY` for embeddings and GPT-4o-mini responses
- ChromaDB (installed via pip, runs in-process — no external service required)
- Python 3.12 or earlier (ChromaDB is not compatible with Python 3.13)

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - RAGService - Ingesting PDF: document.pdf
INFO - RAGService - Extracted 45 chunks from 12 pages
INFO - RAGService - Embedded 45 chunks, stored in ChromaDB
INFO - RAGService - Query: "What are the main findings?"
INFO - RAGService - Retrieved 5 relevant chunks
Answer: The main findings of the document are ...
```

## Notes

- Output varies with the PDF content and question asked
- Chunk count depends on document length and chunking parameters (default: 512 tokens, 50 overlap)
- OpenAI API costs apply for embeddings and completions
- ChromaDB stores vectors in-memory by default; use `persist_directory` for durable storage
