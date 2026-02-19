# OpenAI LLM Connector

Wrap the OpenAI chat API as a Blazing service connector.

## API

```python
from blazing.local.llm import OpenAIConnector, ChatResponse

connector = OpenAIConnector(api_key="sk-...", model="gpt-4o-mini")

# As async context manager
async with OpenAIConnector(...) as connector:
    response: ChatResponse = await connector.chat([
        {"role": "system", "content": "You are helpful."},
        {"role": "user",   "content": "Hello!"},
    ])
    print(response.content)

# Streaming
async for chunk in connector.stream(messages):
    print(chunk.content, end="", flush=True)
```

## ChatResponse Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | `str` | Response text |
| `role` | `str` | Always `"assistant"` |
| `model` | `str` | Model that responded |
| `finish_reason` | `str` | `"stop"`, `"tool_calls"`, etc. |
| `tool_calls` | `list` | Tool calls if any |
| `usage` | `TokenUsage` | `prompt_tokens`, `completion_tokens`, `total_tokens` |

## Patterns

| Pattern | Config |
|---------|--------|
| Single-turn | `chat([{"role": "user", "content": "..."}])` |
| Multi-turn | `chat(full_conversation_list)` |
| Streaming | `async for chunk in stream(messages)` |
| Tool calling | `chat(messages, tools=[...])` |
| Temperature | `chat(messages, temperature=0.0)` |

## Running

```bash
export OPENAI_API_KEY=sk-...
python flow.py
```

For service deployment: `docker-compose up -d` then `app.publish()`.
