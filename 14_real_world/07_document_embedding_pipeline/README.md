# Document Embedding Pipeline

High-throughput document pipeline: S3/local → chunk → embed → MongoDB, with checkpoint/resume.

## Patterns

- Token-based chunking via tiktoken (400 tokens, 80 overlap)
- Dual embedding backends: sentence-transformers (free) or OpenAI ($0.00002/1k tokens)
- `run_in_executor()` for sync sentence-transformers inference
- JSON checkpoint for fault-tolerant batch processing (resume after crashes)
- S3 pagination for buckets >1000 objects

## Setup

```bash
pip install tiktoken sentence-transformers
```

Optionally: `boto3` for S3, `pymongo` for MongoDB, `openai` for OpenAI embeddings.

## Endpoints

- `POST /pipeline/process` — process all documents (S3 or local directory)
- `POST /pipeline/process-single` — process one document
- `GET /pipeline/checkpoint` — view progress
- `DELETE /pipeline/checkpoint` — reset to reprocess all
- `GET /pipeline/stats` — collection statistics
