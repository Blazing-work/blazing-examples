"""
Batched Steps Example for Blazing

@batched automatically collects individual step calls into batches for
efficient processing — GPU inference, bulk DB inserts, batch API calls.

Batching strategy (whichever fires first):
  - Up to max_batch_size items have accumulated, OR
  - wait_ms milliseconds have passed since the first item arrived

The function receives a list and must return a list of the same length.
Individual callers always pass a single item; batching is transparent to them.

No Docker or infrastructure required — decorators apply at publish time.
"""

import os

from blazing import Blazing
from blazing.batched import batched

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Pattern 1: GPU Inference Batching ────────────────────────────────────────

@app.step
@batched(max_batch_size=32, wait_ms=100)
async def classify_text(texts: list, services=None) -> list:
    """
    Classify a batch of texts in one model forward pass.

    Individual callers pass a single string.
    Blazing collects up to 32 callers (or waits 100ms) before dispatching.

    Args:
        texts: Auto-collected list of strings from individual callers.
    Returns:
        List of category labels — one per input, in the same order.
    """
    # In production: run texts through your classifier batch
    # e.g. model.predict(texts)
    return [f"category_{hash(t) % 5}" for t in texts]


# ── Pattern 2: Bulk Database Inserts ─────────────────────────────────────────

@app.step
@batched(max_batch_size=100, wait_ms=50)
async def insert_events(events: list, services=None) -> list:
    """
    Insert events in bulk — 100 individual callers become 1 batch INSERT.

    Each caller passes a single dict; this function receives a list of dicts.
    Returns one record ID per event.
    """
    # In production: bulk INSERT into DB
    # cursor.executemany("INSERT INTO events ...", events)
    return [f"evt_{i}" for i in range(len(events))]


# ── Pattern 3: Batch API Calls ────────────────────────────────────────────────

@app.step
@batched(max_batch_size=10, wait_ms=200)
async def translate_texts(texts: list, services=None) -> list:
    """
    Translate texts via a batched API request.

    wait_ms=200 allows more callers to accumulate, reducing API round-trips
    from N calls to N/10 calls.
    """
    # In production: POST texts to translation API in one request
    return [f"[translated] {t}" for t in texts]


# ── Pattern 4: Embedding Generation ──────────────────────────────────────────

@app.step
@batched(max_batch_size=64, wait_ms=25, pad_to_max=True)
async def generate_embeddings(texts: list, services=None) -> list:
    """
    Generate text embeddings with fixed-size batches.

    pad_to_max=True pads under-full batches to exactly 64 items so the
    embedding model always receives uniform tensor shapes (useful for
    static-shape GPU kernels).
    """
    # In production: model.encode(texts) → list of vectors
    return [[0.1, 0.2, 0.3] for _ in texts]


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Batched Step Patterns:")
    print()
    print("  @batched(max_batch_size=32, wait_ms=100)")
    print("    → GPU classification: collect up to 32 calls or wait 100ms")
    print()
    print("  @batched(max_batch_size=100, wait_ms=50)")
    print("    → Bulk inserts: up to 100 rows per SQL statement")
    print()
    print("  @batched(max_batch_size=10, wait_ms=200)")
    print("    → API rate optimization: 200ms accumulation window")
    print()
    print("  @batched(max_batch_size=64, wait_ms=25, pad_to_max=True)")
    print("    → Fixed-shape batches for static-graph GPU kernels")
    print()
    print("Individual callers always pass a single item.")
    print("Blazing handles accumulation and dispatch transparently.")
    print()
    print("Deploy: app.publish()")
