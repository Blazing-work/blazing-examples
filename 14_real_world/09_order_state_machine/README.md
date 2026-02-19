# Order Processing State Machine

An e-commerce order flows through a multi-state approval pipeline before completing or failing.

## State transitions

```
PENDING → PAYMENT_CHECK → INVENTORY_CHECK → APPROVED → COMPLETED
                        ↘                ↘
                         REJECTED ────────────────────► FAILED
```

## Architecture

| Layer | Component | Runs on |
|---|---|---|
| Service | `OrderService` — payment & inventory lookups | Trusted worker |
| Step | `transition` — one state-machine hop | Pyodide sandbox |
| Workflow | `process_order` — loops until terminal state | Orchestrator |

The **sandboxed step** handles transition logic and calls the **trusted service** for external lookups. This separates user-defined logic (sandbox) from I/O operations (trusted).

## Run

```bash
BLAZING_API_KEY=your-key python flow.py
```
