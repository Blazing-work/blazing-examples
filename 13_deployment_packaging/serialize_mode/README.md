# Serialize Loading Strategy

Use `loading_strategy="serialize"` for fast iteration without a wheel build step.

## Loading Strategies

| Strategy | How code reaches workers | Best for |
|----------|-------------------------|----------|
| `"wheel"` (default) | Build + upload Python wheel | Production, dependencies |
| `"serialize"` | Serialize step functions at runtime | Rapid iteration |
| `"dockerfile"` | Bundle code inside Docker image | Full environment control |

## API

```python
from blazing import Blazing

app = Blazing(
    api_url="...",
    api_token="...",
    loading_strategy="serialize",   # no wheel build needed
)

@app.step
async def process(data: dict, services=None) -> dict:
    ...
```

## Trade-offs

**Serialize** pros:
- Fastest iteration — no `pip wheel` step
- Great for prototyping and local development

**Serialize** cons:
- Functions must be serializable (no unpicklable closures)
- Not suitable for large dependency trees (use `wheel` or `dockerfile`)

## Running

```bash
docker-compose up -d
python flow.py
```
