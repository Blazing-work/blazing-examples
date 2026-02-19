# Egress Policy Example

Controls outbound network access from Blazing service steps.

## What It Does

Declares which external hosts a service is permitted to connect to:

```python
@app.service(egress=["api.openai.com"])          # exact hostname
@app.service(egress=["*.anthropic.com"])          # wildcard subdomain
@app.service(egress=["api.a.com", "api.b.com"])  # multiple destinations
@app.service(egress=[])                           # deny all outbound
```

When a sandboxed worker runs a service step, Blazing installs a `sys.audit`
hook that enforces the allowlist. Undeclared connections raise
`ConnectionRefusedError` with "egress" in the message.

## Enforcement Modes

Set via the `BLAZING_EGRESS_MODE` environment variable:

| Mode | Behaviour |
|------|-----------|
| `DENY_BY_DEFAULT` | Block undeclared destinations (production default) |
| `AUDIT_ONLY` | Log violations without blocking (dry-run rollout) |
| `ALLOW_ALL` | No enforcement (local development) |

## Examples in This File

| Class | Egress | Purpose |
|-------|--------|---------|
| `SummarizationService` | `["api.openai.com"]` | Single API — exact host |
| `ClaudeService` | `["*.anthropic.com"]` | Wildcard subdomain |
| `PaymentAIService` | `["api.openai.com", "api.stripe.com"]` | Multiple APIs |
| `IsolatedComputeService` | `[]` | Zero outbound — pure compute |

## Running Locally

The `IsolatedComputeService.compute_stats` can run without Docker:

```bash
python flow.py
```

Full egress enforcement requires Docker infrastructure:

```bash
docker-compose up -d
python flow.py
```
