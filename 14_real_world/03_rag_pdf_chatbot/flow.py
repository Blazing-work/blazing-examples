"""
RAG PDF Chatbot Example for Blazing

Demonstrates vector search and retrieval-augmented generation (RAG) using:
- PDF text extraction with pdfplumber
- Document chunking with overlap
- OpenAI embeddings (text-embedding-3-small)
- ChromaDB for vector storage
- GPT-4o-mini for context-aware question answering

IMPORTANT: Requires Python 3.12 or earlier (ChromaDB not compatible with 3.13)
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

import pdfplumber
import chromadb
from chromadb.config import Settings
from blazing import Blazing, BaseService
from blazing_service.connectors.openai import OpenAIConnector
from blazing_service.connectors.secrets import SecretsConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=["api.openai.com"])
class RAGService(BaseService):
    """
    RAG (Retrieval-Augmented Generation) service for PDF question answering.

    Workflow:
    1. Ingest PDF -> extract text -> chunk -> embed -> store in ChromaDB
    2. Query -> embed question -> semantic search -> retrieve top chunks -> generate answer with GPT
    """

    def __init__(self, connector_instances=None):
        """Initialize RAG service with OpenAI and ChromaDB."""
        super().__init__(connector_instances)

        self.secrets = connector_instances.get('secrets') if connector_instances else SecretsConnector()
        self.openai = connector_instances.get('openai') if connector_instances else None

        # Initialize ChromaDB with persistent storage
        chroma_db_path = Path(__file__).parent / "chroma_db"
        chroma_db_path.mkdir(exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(
            path=str(chroma_db_path),
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="pdf_documents",
            metadata={"description": "PDF document chunks with embeddings"}
        )

        logger.info(f"RAGService initialized with ChromaDB at {chroma_db_path}")

    async def _ensure_openai_connected(self):
        """Ensure OpenAI connector is initialized and connected."""
        if self.openai is None:
            api_key = await self.secrets.get("OPENAI_API_KEY")
            self.openai = OpenAIConnector(api_key=api_key)

        if not self.openai.is_connected:
            await self.openai.connect()

    def _chunk_text(self, text: str, chunk_size: int = 400, overlap: int = 80) -> List[str]:
        """
        Split text into overlapping chunks.

        Uses word-based chunking (400 words, 80 overlap ≈ 20%).
        For production, use tiktoken for token-accurate chunking.
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if chunk_words:
                chunks.append(" ".join(chunk_words))

        return chunks

    async def ingest_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Ingest PDF: extract text, chunk, embed, and store in ChromaDB.

        Returns:
            Dictionary with ingestion status and chunk count
        """
        await self._ensure_openai_connected()

        logger.info(f"Ingesting PDF: {pdf_path}")

        # Extract text page by page (avoids loading entire PDF into memory)
        all_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    all_text.append(text)
                    logger.debug(f"Extracted {len(text)} chars from page {page_num}")

        full_text = "\n".join(all_text)
        logger.info(f"Extracted {len(full_text)} total characters from PDF")

        chunks = self._chunk_text(full_text, chunk_size=400, overlap=80)
        logger.info(f"Created {len(chunks)} chunks from PDF text")

        # Generate embeddings for all chunks
        embeddings = []
        for chunk in chunks:
            embedding = await self.openai.embed(chunk, model="text-embedding-3-small")
            embeddings.append(embedding)

        logger.info(f"Generated {len(embeddings)} embeddings")

        # Store in ChromaDB
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{"source": pdf_path, "chunk_index": i} for i in range(len(chunks))]
        )

        logger.info(f"Stored {len(chunks)} chunks in ChromaDB collection")

        return {
            "status": "ingested",
            "chunks": len(chunks),
            "source": pdf_path
        }

    async def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Query the RAG system: embed question, search, generate answer.

        Returns:
            Dictionary with answer and metadata
        """
        await self._ensure_openai_connected()

        logger.info(f"Querying: {question}")

        question_embedding = await self.openai.embed(question, model="text-embedding-3-small")

        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results=top_k
        )

        retrieved_chunks = results['documents'][0] if results['documents'] else []
        context = "\n\n".join(retrieved_chunks)

        logger.info(f"Retrieved {len(retrieved_chunks)} relevant chunks")

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. If the context doesn't contain relevant information, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]

        response = await self.openai.chat(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=500
        )

        answer = response['choices'][0]['message']['content']

        return {
            "answer": answer,
            "question": question,
            "chunks_retrieved": len(retrieved_chunks),
            "tokens_used": response['usage']['total_tokens']
        }


@app.endpoint.post("/ingest")
async def ingest_endpoint(request, services=None):
    """
    Upload and ingest a PDF file.

    Expects multipart form data with 'file' field containing PDF.

    Returns:
        JSON with ingestion status and chunk count
    """
    form = await request.form()

    if 'file' not in form:
        return {"error": "No file provided"}, 400

    file = form['file']

    temp_path = Path("/tmp") / file.filename
    with open(temp_path, 'wb') as f:
        f.write(await file.read())

    rag_service = services['RAGService']

    try:
        result = await rag_service.ingest_pdf(str(temp_path))
        return result
    finally:
        temp_path.unlink(missing_ok=True)


@app.endpoint.post("/query")
async def query_endpoint(request, services=None):
    """
    Query the RAG chatbot.

    Expects JSON: {"question": "What is Blazing Flow?"}

    Returns:
        JSON with answer and metadata
    """
    data = await request.json()

    if 'question' not in data:
        return {"error": "No question provided"}, 400

    rag_service = services['RAGService']
    result = await rag_service.query(data['question'])
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
