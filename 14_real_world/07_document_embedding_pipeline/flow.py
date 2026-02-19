"""
Document Embedding Pipeline Example for Blazing

Demonstrates high-throughput document processing pipeline with:
- S3 batch download (with local file fallback for testing)
- Token-based text chunking with overlap (tiktoken)
- Dual embedding backends: sentence-transformers (free) and OpenAI (paid)
- MongoDB vector storage
- Checkpoint/resume for fault tolerance

Production patterns:
- Load embedding model in connect() (not per-request, avoid 5-minute download)
- S3 pagination for large buckets (>1000 objects)
- Token-based chunking (400 tokens, 80 overlap) for embedding alignment
- run_in_executor for sync sentence-transformers library
- JSON file checkpoint tracking (Redis alternative included)
- Batch embedding processing for efficiency
"""

import os
import logging
import json
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timezone

import tiktoken
from sentence_transformers import SentenceTransformer

from blazing import Blazing, BaseService
from blazing_service.connectors.s3 import S3Connector
from blazing_service.connectors.mongodb import MongoDBConnector
from blazing_service.connectors.openai import OpenAIConnector
from blazing_service.connectors.secrets import SecretsConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blazing app
app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=["s3.amazonaws.com", "huggingface.co"])
class EmbeddingPipelineService(BaseService):
    """
    Document embedding pipeline with S3/local sources, chunking, and MongoDB storage.

    Pipeline flow:
    1. List documents from S3 or local directory
    2. Download and chunk text (400 tokens, 80 overlap via tiktoken)
    3. Generate embeddings (sentence-transformers or OpenAI)
    4. Store chunks with embeddings in MongoDB
    5. Track progress with checkpoint (resume after crashes)

    Embedding backends:
    - sentence-transformers all-MiniLM-L6-v2: Free, 384-dim, local, ~120MB download
    - OpenAI text-embedding-3-small: $0.00002/1k tokens, 1536-dim, API-based

    Checkpoint enables fault-tolerant batch processing of large document collections.
    """

    def __init__(self, connector_instances=None):
        """Initialize embedding pipeline service."""
        super().__init__(connector_instances)

        # Initialize connectors
        self.secrets = connector_instances.get('secrets') if connector_instances else SecretsConnector()
        self.s3 = connector_instances.get('s3') if connector_instances else None
        self.mongo = connector_instances.get('mongodb') if connector_instances else None
        self.openai = connector_instances.get('openai') if connector_instances else None

        # sentence-transformers model (loaded in connect(), not per-request)
        self.model = None

        # Token counter for chunking (cl100k_base for alignment with OpenAI models)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

        # Checkpoint file path
        self.checkpoint_path = Path(__file__).parent / "checkpoint.json"

        logger.info("EmbeddingPipelineService initialized")

    async def connect(self):
        """
        Load sentence-transformers model on service startup.

        CRITICAL: Model loaded here, not per-request.
        First download is ~120MB from HuggingFace, takes minutes.
        Subsequent loads use cached model (~5 seconds from disk).

        Set SENTENCE_TRANSFORMERS_HOME env var to control cache location.
        """
        # Ensure connectors are connected
        if self.s3 and not self.s3.is_connected:
            await self.s3.connect()

        if self.mongo and not self.mongo.is_connected:
            await self.mongo.connect()

        # Load sentence-transformers model in executor (blocking operation)
        loop = asyncio.get_event_loop()
        self.model = await loop.run_in_executor(
            None,
            self._load_sentence_transformer_model
        )

        logger.info(
            "EmbeddingPipelineService connected "
            "(sentence-transformers model loaded, ready for embedding)"
        )

    def _load_sentence_transformer_model(self) -> SentenceTransformer:
        """
        Load sentence-transformers model synchronously.

        Uses all-MiniLM-L6-v2:
        - 384-dimensional embeddings
        - Fast inference on CPU
        - Good for semantic similarity
        - ~120MB download on first run
        """
        model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("sentence-transformers model 'all-MiniLM-L6-v2' loaded (384-dim)")
        return model

    async def list_documents_s3(
        self,
        bucket: str,
        prefix: str = ""
    ) -> List[Dict[str, Any]]:
        """
        List all documents in S3 bucket with pagination.

        S3 list_objects_v2 returns max 1000 objects per request.
        This method loops until all objects are fetched.

        Args:
            bucket: S3 bucket name
            prefix: Filter by key prefix (e.g., "documents/")

        Returns:
            List of document metadata dicts:
            - key: S3 object key
            - size: Size in bytes
            - last_modified: ISO timestamp
        """
        if not self.s3:
            raise ValueError("S3 connector not initialized")

        documents = []
        continuation_token = None

        while True:
            # Fetch batch (max 1000 objects)
            batch = await self.s3.list_objects(
                bucket=bucket,
                prefix=prefix,
                max_keys=1000
            )

            documents.extend(batch)

            # Check if more pages exist
            if len(batch) < 1000:
                break

        logger.info(f"Listed {len(documents)} documents from s3://{bucket}/{prefix}")
        return documents

    def list_documents_local(
        self,
        directory: str
    ) -> List[Dict[str, Any]]:
        """
        List documents in local directory.

        Supports .txt, .md, .pdf extensions.

        Args:
            directory: Local directory path

        Returns:
            List of document metadata dicts:
            - key: File path relative to directory
            - size: File size in bytes
            - last_modified: ISO timestamp
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise ValueError(f"Directory not found: {directory}")

        documents = []
        for ext in ['*.txt', '*.md', '*.pdf']:
            for file_path in dir_path.rglob(ext):
                if file_path.is_file():
                    stat = file_path.stat()
                    documents.append({
                        'key': str(file_path.relative_to(dir_path)),
                        'size': stat.st_size,
                        'last_modified': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                    })

        logger.info(f"Listed {len(documents)} documents from {directory}")
        return documents

    async def download_document_s3(
        self,
        bucket: str,
        key: str
    ) -> str:
        """
        Download document from S3 and decode as UTF-8 text.

        Args:
            bucket: S3 bucket name
            key: S3 object key

        Returns:
            Document text content
        """
        if not self.s3:
            raise ValueError("S3 connector not initialized")

        data = await self.s3.download(bucket=bucket, key=key)
        text = data.decode('utf-8')
        logger.info(f"Downloaded s3://{bucket}/{key} ({len(text)} chars)")
        return text

    def read_document_local(
        self,
        directory: str,
        key: str
    ) -> str:
        """
        Read document from local filesystem.

        Args:
            directory: Base directory path
            key: File path relative to directory

        Returns:
            Document text content
        """
        file_path = Path(directory) / key
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        text = file_path.read_text(encoding='utf-8')
        logger.info(f"Read {file_path} ({len(text)} chars)")
        return text

    def chunk_text(
        self,
        text: str,
        source: str,
        chunk_size: int = 400,
        overlap: int = 80
    ) -> List[Dict[str, Any]]:
        """
        Chunk text into overlapping segments using token-based splitting.

        Uses tiktoken (cl100k_base encoding) for accurate token counting.
        Token-based chunking (not character-based) aligns with embedding models.

        Args:
            text: Document text to chunk
            source: Source identifier (S3 key or file path)
            chunk_size: Target tokens per chunk (default: 400)
            overlap: Overlap tokens between chunks (default: 80, 20%)

        Returns:
            List of chunk dicts:
            - text: Chunk text content
            - source: Source identifier
            - chunk_index: 0-based chunk index
            - token_count: Actual tokens in chunk
        """
        # Encode text to tokens
        tokens = self.tokenizer.encode(text)

        # Create overlapping chunks
        chunks = []
        stride = chunk_size - overlap  # Step size

        for i in range(0, len(tokens), stride):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_index": len(chunks),
                "token_count": len(chunk_tokens)
            })

        logger.info(
            f"Chunked document '{source}' into {len(chunks)} chunks "
            f"({chunk_size} tokens, {overlap} overlap)"
        )
        return chunks

    async def embed_chunks_sentence_transformers(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings using sentence-transformers (local, free).

        model.encode() is synchronous, wrapped in run_in_executor.
        Processes all chunks in a single batch for efficiency.

        Args:
            chunks: List of chunk dicts with 'text' field

        Returns:
            Chunks with added 'embedding' field (384-dim list of floats)
        """
        if not self.model:
            raise ValueError("sentence-transformers model not loaded")

        texts = [chunk['text'] for chunk in chunks]

        # Generate embeddings in executor (blocking operation)
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            lambda: self.model.encode(texts, convert_to_numpy=True).tolist()
        )

        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i]

        logger.info(
            f"Generated {len(chunks)} embeddings via sentence-transformers "
            f"(384-dim, all-MiniLM-L6-v2)"
        )
        return chunks

    async def embed_chunks_openai(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings using OpenAI text-embedding-3-small.

        Args:
            chunks: List of chunk dicts with 'text' field

        Returns:
            Chunks with added 'embedding' field (1536-dim list of floats)
        """
        if not self.openai:
            # Initialize OpenAI connector if not provided
            api_key = await self.secrets.get("OPENAI_API_KEY")
            self.openai = OpenAIConnector(api_key=api_key)
            await self.openai.connect()

        texts = [chunk['text'] for chunk in chunks]

        # Generate embeddings via OpenAI API
        embeddings = await self.openai.embed(
            texts=texts,
            model="text-embedding-3-small"
        )

        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i]

        logger.info(
            f"Generated {len(chunks)} embeddings via OpenAI "
            f"(1536-dim, text-embedding-3-small)"
        )
        return chunks

    async def store_embeddings(
        self,
        collection: str,
        chunks: List[Dict[str, Any]]
    ) -> int:
        """
        Store chunks with embeddings in MongoDB collection.

        MongoDB supports arrays for embedding storage.
        No special vector extension needed (Atlas has vector search).

        Args:
            collection: MongoDB collection name
            chunks: List of chunk dicts with embeddings

        Returns:
            Number of chunks stored
        """
        if not self.mongo:
            # Initialize MongoDB connector if not provided
            self.mongo = MongoDBConnector(
                name="mongodb",
                secrets=self.secrets
            )
            await self.mongo.connect()

        # Add created_at timestamp
        for chunk in chunks:
            chunk['created_at'] = datetime.now(timezone.utc).isoformat()

        # Insert chunks (use insert_many if available, else loop)
        # For now, use individual inserts (can optimize later)
        for chunk in chunks:
            await self.mongo.insert(
                collection=collection,
                document=chunk
            )

        logger.info(f"Stored {len(chunks)} chunks in MongoDB collection '{collection}'")
        return len(chunks)

    async def process_document(
        self,
        source: str,
        source_type: str,  # "s3" or "local"
        bucket_or_directory: str,
        key: str,
        collection: str,
        use_openai: bool = False,
        chunk_size: int = 400,
        overlap: int = 80
    ) -> Dict[str, Any]:
        """
        Full pipeline for single document: download → chunk → embed → store.

        Args:
            source: Source identifier for logging
            source_type: "s3" or "local"
            bucket_or_directory: S3 bucket name or local directory path
            key: S3 object key or file path relative to directory
            collection: MongoDB collection name
            use_openai: Use OpenAI embeddings instead of sentence-transformers
            chunk_size: Tokens per chunk
            overlap: Overlap tokens

        Returns:
            Processing stats:
            - source: Source identifier
            - chunks_created: Number of chunks
            - chunks_stored: Number of chunks stored in MongoDB
        """
        # Download document
        if source_type == "s3":
            text = await self.download_document_s3(bucket_or_directory, key)
        elif source_type == "local":
            text = self.read_document_local(bucket_or_directory, key)
        else:
            raise ValueError(f"Invalid source_type: {source_type}")

        # Chunk text
        chunks = self.chunk_text(
            text=text,
            source=source,
            chunk_size=chunk_size,
            overlap=overlap
        )

        # Generate embeddings
        if use_openai:
            chunks_with_embeddings = await self.embed_chunks_openai(chunks)
        else:
            chunks_with_embeddings = await self.embed_chunks_sentence_transformers(chunks)

        # Store in MongoDB
        stored_count = await self.store_embeddings(
            collection=collection,
            chunks=chunks_with_embeddings
        )

        return {
            "source": source,
            "chunks_created": len(chunks),
            "chunks_stored": stored_count
        }

    def load_checkpoint(self) -> Dict[str, Any]:
        """
        Load checkpoint from JSON file.

        Checkpoint tracks:
        - processed: List of document keys that have been processed
        - last_updated: ISO timestamp of last update

        Returns:
            Checkpoint dict (or empty dict if no checkpoint exists)
        """
        if not self.checkpoint_path.exists():
            return {"processed": [], "last_updated": None}

        try:
            with open(self.checkpoint_path, 'r') as f:
                checkpoint = json.load(f)
            logger.info(
                f"Loaded checkpoint: {len(checkpoint.get('processed', []))} documents processed"
            )
            return checkpoint
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}, starting fresh")
            return {"processed": [], "last_updated": None}

    def save_checkpoint(self, checkpoint: Dict[str, Any]):
        """
        Save checkpoint to JSON file.

        Args:
            checkpoint: Checkpoint dict to save
        """
        checkpoint['last_updated'] = datetime.now(timezone.utc).isoformat()

        with open(self.checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(
            f"Saved checkpoint: {len(checkpoint.get('processed', []))} documents processed"
        )

    def reset_checkpoint(self):
        """Delete checkpoint file to reprocess all documents."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            logger.info("Checkpoint reset (deleted)")
        else:
            logger.info("No checkpoint to reset")

    async def process_batch_with_checkpoint(
        self,
        source_type: str,  # "s3" or "local"
        bucket_or_directory: str,
        prefix: str = "",
        collection: str = "embeddings",
        use_openai: bool = False,
        chunk_size: int = 400,
        overlap: int = 80
    ) -> Dict[str, Any]:
        """
        Process all documents in batch with checkpoint/resume.

        Checkpoint tracks processed documents. On restart, skips already-processed ones.
        This enables fault-tolerant processing of large document collections.

        Args:
            source_type: "s3" or "local"
            bucket_or_directory: S3 bucket name or local directory path
            prefix: Prefix filter for S3 or subdirectory for local
            collection: MongoDB collection name
            use_openai: Use OpenAI embeddings instead of sentence-transformers
            chunk_size: Tokens per chunk
            overlap: Overlap tokens

        Returns:
            Processing stats:
            - total: Total documents found
            - processed: Documents processed in this run
            - skipped: Documents skipped (already in checkpoint)
            - chunks_created: Total chunks created
            - errors: Number of errors encountered
        """
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        processed_set = set(checkpoint.get('processed', []))

        # List documents
        if source_type == "s3":
            documents = await self.list_documents_s3(bucket_or_directory, prefix)
        elif source_type == "local":
            # For local, use prefix as subdirectory
            search_dir = str(Path(bucket_or_directory) / prefix) if prefix else bucket_or_directory
            documents = self.list_documents_local(search_dir)
        else:
            raise ValueError(f"Invalid source_type: {source_type}")

        # Process documents
        stats = {
            "total": len(documents),
            "processed": 0,
            "skipped": 0,
            "chunks_created": 0,
            "errors": 0
        }

        for doc in documents:
            key = doc['key']

            # Skip if already processed
            if key in processed_set:
                stats['skipped'] += 1
                logger.info(f"Skipping {key} (already processed)")
                continue

            try:
                # Process document
                result = await self.process_document(
                    source=key,
                    source_type=source_type,
                    bucket_or_directory=bucket_or_directory,
                    key=key,
                    collection=collection,
                    use_openai=use_openai,
                    chunk_size=chunk_size,
                    overlap=overlap
                )

                stats['processed'] += 1
                stats['chunks_created'] += result['chunks_created']

                # Update checkpoint after each successful document
                checkpoint['processed'].append(key)
                self.save_checkpoint(checkpoint)

                logger.info(
                    f"Processed {key}: {result['chunks_created']} chunks "
                    f"({stats['processed']}/{stats['total']})"
                )

            except Exception as e:
                stats['errors'] += 1
                logger.error(f"Failed to process {key}: {e}")
                # Continue with next document (don't add to checkpoint)

        return stats


@app.endpoint.post("/pipeline/process")
async def process_documents(request, services=None):
    """
    Process all documents from S3 or local directory.

    Body:
    {
        "source": "local" | "s3",
        "path": "/path/to/sample_docs" | "my-bucket",
        "prefix": "" | "documents/",
        "collection": "embeddings",
        "use_openai": false,
        "chunk_size": 400,
        "overlap": 80
    }

    Returns:
    {
        "total": 10,
        "processed": 7,
        "skipped": 3,
        "chunks_created": 45,
        "errors": 0
    }
    """
    body = await request.json()
    pipeline = services['EmbeddingPipelineService']

    stats = await pipeline.process_batch_with_checkpoint(
        source_type=body.get('source', 'local'),
        bucket_or_directory=body['path'],
        prefix=body.get('prefix', ''),
        collection=body.get('collection', 'embeddings'),
        use_openai=body.get('use_openai', False),
        chunk_size=body.get('chunk_size', 400),
        overlap=body.get('overlap', 80)
    )

    return stats


@app.endpoint.post("/pipeline/process-single")
async def process_single_document(request, services=None):
    """
    Process a single document.

    Body:
    {
        "source": "local" | "s3",
        "path": "/path/to/sample_docs" | "my-bucket",
        "key": "blazing_overview.txt",
        "collection": "embeddings",
        "use_openai": false,
        "chunk_size": 400,
        "overlap": 80
    }

    Returns:
    {
        "source": "blazing_overview.txt",
        "chunks_created": 3,
        "chunks_stored": 3
    }
    """
    body = await request.json()
    pipeline = services['EmbeddingPipelineService']

    result = await pipeline.process_document(
        source=body['key'],
        source_type=body.get('source', 'local'),
        bucket_or_directory=body['path'],
        key=body['key'],
        collection=body.get('collection', 'embeddings'),
        use_openai=body.get('use_openai', False),
        chunk_size=body.get('chunk_size', 400),
        overlap=body.get('overlap', 80)
    )

    return result


@app.endpoint.get("/pipeline/checkpoint")
async def get_checkpoint(request, services=None):
    """
    View current checkpoint state.

    Returns:
    {
        "processed": ["doc1.txt", "doc2.txt"],
        "last_updated": "2026-02-06T08:00:00Z",
        "count": 2
    }
    """
    pipeline = services['EmbeddingPipelineService']
    checkpoint = pipeline.load_checkpoint()

    return {
        "processed": checkpoint.get('processed', []),
        "last_updated": checkpoint.get('last_updated'),
        "count": len(checkpoint.get('processed', []))
    }


@app.endpoint.delete("/pipeline/checkpoint")
async def reset_checkpoint(request, services=None):
    """
    Reset checkpoint to reprocess all documents.

    Returns:
    {
        "message": "Checkpoint reset"
    }
    """
    pipeline = services['EmbeddingPipelineService']
    pipeline.reset_checkpoint()

    return {"message": "Checkpoint reset"}


@app.endpoint.get("/pipeline/stats")
async def get_stats(request, services=None):
    """
    Get pipeline statistics.

    Query params:
    - collection: MongoDB collection name (default: embeddings)

    Returns:
    {
        "collection": "embeddings",
        "total_chunks": 150,
        "unique_sources": 10,
        "checkpoint_count": 8
    }
    """
    pipeline = services['EmbeddingPipelineService']
    collection = request.query.get('collection', 'embeddings')

    # Get checkpoint info
    checkpoint = pipeline.load_checkpoint()

    # Get MongoDB stats (if connected)
    total_chunks = 0
    unique_sources = 0

    if pipeline.mongo:
        # Count total chunks
        chunks = await pipeline.mongo.find(
            collection=collection,
            filter={},
            limit=10000
        )
        total_chunks = len(chunks)

        # Count unique sources
        sources = set(chunk.get('source') for chunk in chunks)
        unique_sources = len(sources)

    return {
        "collection": collection,
        "total_chunks": total_chunks,
        "unique_sources": unique_sources,
        "checkpoint_count": len(checkpoint.get('processed', []))
    }


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
