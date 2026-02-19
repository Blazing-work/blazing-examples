# Direct Function Call Pattern

`@app.step` and `@app.workflow` decorated functions are **callable as plain Python functions** — no backend, no `publish()`, no infrastructure.

## When to use this

- **Unit testing steps** in isolation without Docker
- **Local development** — iterate on logic before deploying
- **CI pipelines** — run logic tests without credentials

## How it works

The decorator checks an internal `enqueue_var` contextvar:

- **Outside the executor** (direct call): `enqueue_var=False` → runs in-process, returns result
- **Inside a running workflow** (distributed): `enqueue_var=True` → enqueues to backend

Same decorated function, two behaviors based on context.

## Run

```bash
python flow.py
```

No `BLAZING_API_KEY` or Docker needed.
