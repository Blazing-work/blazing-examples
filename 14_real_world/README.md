# 14. Real-World Applications

Complete, production-ready application examples built on Blazing. Each demonstrates a distinct pattern and integrates multiple services.

| Example | Pattern | Key Dependencies |
|---------|---------|-----------------|
| [01_hackernews_slackbot](01_hackernews_slackbot/) | Scheduled workflow + HTTP endpoint | httpx, Slack connector |
| [02_sql_explorer](02_sql_explorer/) | Read-only SQL API with safety checks | duckdb |
| [03_rag_pdf_chatbot](03_rag_pdf_chatbot/) | RAG with vector search | pdfplumber, chromadb, OpenAI (**Python ≤3.12**) |
| [04_ocr_job_queue](04_ocr_job_queue/) | Async job queue with status polling | OpenAI Vision, Redis |
| [05_docsearch_crawler](05_docsearch_crawler/) | BFS web crawler with indexing | trafilatura, beautifulsoup4, Algolia |
| [06_sheets_mongo_sync](06_sheets_mongo_sync/) | Bidirectional data sync (last-write-wins) | Google Sheets connector, MongoDB connector |
| [07_document_embedding_pipeline](07_document_embedding_pipeline/) | Batch ML pipeline with checkpoint/resume | tiktoken, sentence-transformers, MongoDB, S3 |
| [08_satellite_image_vectors](08_satellite_image_vectors/) | Geospatial ML with vector indexing | rasterio, numpy, MongoDB |

## Patterns Demonstrated

- **Scheduled workflows**: `@app.workflow(schedule=Period(hours=1))` auto-triggers on a timer
- **Egress control**: `@app.service(egress=[...])` declares allowed external domains
- **Async job queues**: Submit → Redis state → background process → poll status
- **Service injection**: `connector_instances=None` default with optional connector access
- **Parallel I/O**: `asyncio.Semaphore` + `asyncio.gather` for concurrent API calls
- **Fault tolerance**: Checkpoint/resume pattern for large batch jobs
