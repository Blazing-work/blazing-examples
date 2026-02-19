# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 21}
```

## Notes

- `7 * 3 = 21` — the multiply step triples x=7
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates `version_pins` on a workflow to pin service versions: `@app.workflow(version_pins={'MathService': '1.0.0'})`
