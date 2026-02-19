# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Egress Policy Patterns:

  @app.service(egress=['api.openai.com'])
    → exact hostname match

  @app.service(egress=['*.anthropic.com'])
    → wildcard subdomain (any *.anthropic.com host)

  @app.service(egress=['api.a.com', 'api.b.com'])
    → multiple destinations

  @app.service(egress=[])
    → deny ALL outbound (maximum isolation)

  @app.service()
    → no restriction (development / legacy mode)

Enforcement modes via BLAZING_EGRESS_MODE:
  DENY_BY_DEFAULT  → block undeclared  [production default]
  AUDIT_ONLY       → log, never block  [dry-run]
  ALLOW_ALL        → no enforcement    [local dev]

IsolatedComputeService.compute_stats([1,2,3,4,5]) = {'count': 5, 'total': 15, 'mean': 3.0, 'min': 1, 'max': 5}
```

## Notes

- Runs locally without Docker — the `__main__` block demonstrates patterns and runs `IsolatedComputeService` directly
- `compute_stats([1,2,3,4,5])`: count=5, total=15, mean=3.0, min=1, max=5
- The egress enforcement only applies when services run on Blazing workers — the pattern descriptions are purely local
