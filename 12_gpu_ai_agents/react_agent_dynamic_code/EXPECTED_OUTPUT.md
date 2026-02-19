# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- Running Blazing infrastructure: `docker-compose up -d`
- `BLAZING_API_URL` (defaults to `http://localhost:8000`)
- `BLAZING_API_TOKEN` (defaults to `demo-token-placeholder`)

## Output

```
=== ReAct Agent as Dynamic Code Demo ===

Architecture:
  Pyodide sandbox (react_agent_loop) -> LLMService (trusted) -> mock LLM
  Pyodide sandbox (react_agent_loop) -> ToolService (trusted) -> mock tools
  Pyodide sandbox (react_agent_loop) -> StateService (trusted) -> in-memory store

Signing key generated: a3f2c1d4e5b6f7a8...

--- Invocation 1: New session ---
  Session ID: a3f2c1d4-e5b6-f7a8-9012-3456789abcde
  Steps taken: 2
  Response: Based on my research, here is the answer to: Research the LangGraph architecture

--- Invocation 2: Resume session ---
  Session ID: a3f2c1d4-e5b6-f7a8-9012-3456789abcde (same session)
  Total messages: 8
  Response: Based on my research, here is the answer to: Summarize your findings
```

## Notes

- Session IDs are random UUIDs — actual values will differ each run
- The mock LLMService always performs one tool call (search) then returns a final answer
- In production, replace the mock chat logic with a real LLM connector
- StateService stores sessions in-memory; for production use DictConnector backed by Redis
- The agent loop runs entirely in the Pyodide sandbox — trusted services never expose credentials
