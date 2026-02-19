# Batched Steps

Automatically collect individual step calls into batches for efficient bulk processing.

## How It Works

`@batched` wraps an `@app.step` function. Individual callers each pass **one item**; Blazing accumulates calls and dispatches when either condition fires first:

- **`max_batch_size`** items have arrived, OR
- **`wait_ms`** milliseconds have elapsed since the first item

The function receives a `list` and must return a `list` of the same length (one result per input, in the same order).

## API

```python
from blazing.batched import batched

@app.step
@batched(max_batch_size=32, wait_ms=100)
async def classify_text(texts: list, services=None) -> list:
    return [model.predict(t) for t in texts]   # or model.predict_batch(texts)
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_batch_size` | 32 | Maximum items per batch |
| `wait_ms` | 100.0 | Max wait (ms) after first item arrives |
| `pad_to_max` | False | Pad under-full batches to exactly `max_batch_size` |

## Use Cases

| Pattern | Config | Why |
|---------|--------|-----|
| GPU inference | `max_batch=32, wait=100ms` | One model forward pass per batch |
| Bulk DB inserts | `max_batch=100, wait=50ms` | One `INSERT … VALUES` per batch |
| Translation API | `max_batch=10, wait=200ms` | Minimize round-trips |
| Fixed-shape kernels | `max_batch=64, pad_to_max=True` | Uniform tensor shapes |

## Running

```bash
python flow.py
```

No Docker required — the decorator is applied at publish time.
