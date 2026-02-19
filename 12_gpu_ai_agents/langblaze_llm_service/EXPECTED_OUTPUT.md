# Expected Output

## Running

```bash
OPENAI_API_KEY=your-key python flow.py
```

## Requirements

This example requires external services configured:
- `OPENAI_API_KEY` environment variable
- Running Blazing infrastructure: `docker-compose up -d`

## Output

```
=== LangBlaze LLM Service Demo ===

Architecture:
  Sandboxed step → LLM(services) → LLMService (trusted) → OpenAI

  [question  ] What is the capital of France?
  [command   ] Delete all files in /tmp
  [statement ] The sky is blue.

--- LangChain LCEL ---
{2-sentence explanation of LangChain LCEL}

--- Pyodide sandbox ---
{2-sentence explanation of Pyodide sandbox}
```

## Notes

- If `OPENAI_API_KEY` is not set, the script exits with: `Set OPENAI_API_KEY to run this example.`
- Intent classifications and LCEL explanations are LLM-generated — actual output will vary
- The LLM adapter routes through `LLMService` on trusted workers — the sandbox never sees the API key
