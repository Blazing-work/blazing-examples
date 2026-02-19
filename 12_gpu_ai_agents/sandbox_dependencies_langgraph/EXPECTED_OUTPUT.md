# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'prompt': 'summarize logs', 'status': 'ready'}
```

## Notes

- The step returns the prompt and 'ready' status — it is a placeholder for LangGraph agent integration
- Requires a running Blazing infrastructure: `docker-compose up -d`
- `sandbox_dependencies=['langchain-core']` installs LangChain into the Pyodide sandbox
