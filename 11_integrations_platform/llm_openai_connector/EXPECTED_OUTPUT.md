# Expected Output

## Running

```bash
OPENAI_API_KEY=your-key python flow.py
```

## Requirements

This example requires an OpenAI API key:
- Set `OPENAI_API_KEY` environment variable

## Output

```
=== OpenAI LLM Connector Demo ===

Chat: 2 + 2 equals 4.
Multi-turn: Your name is Alex.

Response fields: content, role, model, finish_reason, usage
usage: {prompt_tokens, completion_tokens, total_tokens}
```

## Notes

- If `OPENAI_API_KEY` is not set, the script exits with: `Set OPENAI_API_KEY to run this example.`
- Chat responses are non-deterministic — actual text from the model will vary
- Does not require docker-compose — the OpenAI connector runs standalone via `async with OpenAIConnector(...)`
