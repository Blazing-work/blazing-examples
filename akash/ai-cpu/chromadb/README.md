# chromadb

Chroma is an open-source embedding database designed for AI applications with native support for storing and querying embeddings.

## Use Cases

- Semantic search
- Retrieval-augmented generation (RAG)
- Recommendation systems
- AI/ML feature stores

## Getting Started

1. Install the client: `pip install chromadb-client`
2. Create a collection and add embeddings
3. Query with natural language or embedding vectors

## Accessing the Service

Use the Chroma Python client:
```python
import chromadb
client = chromadb.HttpClient(host="{SERVICE_URI}", port=8000)
```
Or call the REST API at `http://{SERVICE_URI}:8000/api/v1`.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `IS_PERSISTENT` | `TRUE` |
| `PERSIST_DIRECTORY` | `/mnt/data/chromadb/chroma` |
| `ANONYMIZED_TELEMETRY` | `FALSE` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `chromadb/chroma` |
| CPU | 4.0 |
| Memory | 4Gb |
| Storage | 1Gi |
| Exposed Ports | 8000 |

## Documentation

For full documentation, visit: [https://docs.trychroma.com/](https://docs.trychroma.com/)
