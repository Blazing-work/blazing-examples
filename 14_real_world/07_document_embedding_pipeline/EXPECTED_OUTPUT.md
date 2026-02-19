# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- AWS S3 credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET`)
- MongoDB connection string (`MONGODB_URI`)
- Optional: `OPENAI_API_KEY` for OpenAI embeddings (falls back to sentence-transformers)
- Running Blazing infrastructure: `docker-compose up -d`

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - EmbeddingPipeline - Loading embedding model (first run may take 5+ minutes)...
INFO - EmbeddingPipeline - Model loaded: all-MiniLM-L6-v2 (384-dim)
INFO - EmbeddingPipeline - Processing 50 documents from S3
INFO - EmbeddingPipeline - Chunked 50 docs into 3,240 chunks (400 tokens, 80 overlap)
INFO - EmbeddingPipeline - Embedded and stored 3,240 chunks in MongoDB
{"documents_processed": 50, "chunks_created": 3240, "elapsed_s": 127.4}
```

## Notes

- Document and chunk counts depend on S3 bucket contents
- First run downloads the sentence-transformers model (can take several minutes)
- Checkpoint/resume: already-embedded documents are skipped on subsequent runs
- OpenAI embedding dimensions differ (1536 for ada-002, 3072 for text-embedding-3-large)
