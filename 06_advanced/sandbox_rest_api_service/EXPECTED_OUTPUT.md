# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'test': True}
```

## Notes

- This is a sandbox example with both flow.py and sandbox.py
- Running flow.py executes the sandbox code using run_sandboxed()
- The sandbox code runs in an isolated WASM environment
- Actual output depends on the sandbox.py implementation (not shown in flow.py)
- The example demonstrates REST API service calls from sandboxed code
- Requires Blazing infrastructure (SaaS or local emulator) for sandbox execution
- flow.py reads sandbox.py at runtime and executes it securely
