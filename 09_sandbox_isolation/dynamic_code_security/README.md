# Dynamic Code Security Example

Demonstrates Blazing's 5-layer security model for executing user-submitted functions safely.

## Security Layers

| Layer | Where | What it does |
|-------|-------|--------------|
| 1 | Client (serialize) | AST validation — rejects `import os`, `import subprocess`, etc. |
| 2 | Client (serialize) | HMAC-SHA256 signs the serialized blob |
| 3 | Executor (execute) | Verifies signature **before** deserialization |
| 4 | Executor (execute) | Inspects bytecode after deserialization |
| 5 | Executor (runtime) | Pyodide sandbox isolation (production workers) |

## API

```python
from blazing.dynamic_code import create_signing_key, serialize_user_function, execute_signed_function
from blazing.security import SecurityError

# Generate a shared key (store in secrets manager, share with executor)
signing_key = create_signing_key()

# CLIENT: validate + sign user function
serialized, signature = serialize_user_function(
    user_fn,
    signing_key=signing_key,
    validate=True,          # Layer 1: AST check
)

# EXECUTOR: verify + execute
result = await execute_signed_function(
    serialized,
    signature,
    args=(input_data,),
    signing_key=signing_key,
    validate_bytecode=True, # Layer 4: bytecode check
)
```

## What Layer 1 Blocks

```python
def bad(x):
    import os            # blocked — filesystem access
    import subprocess    # blocked — shell execution
    import sys           # blocked — interpreter access
    return x
```

## Running the Example

No Docker or infrastructure needed:

```bash
python flow.py
```
