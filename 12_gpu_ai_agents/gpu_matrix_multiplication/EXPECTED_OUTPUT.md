# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'device': 'cuda', 'shape': [512, 512]}
```

## Notes

- Output device depends on hardware: `cuda` (NVIDIA GPU), `mps` (Apple Silicon), or `cpu`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The step is tagged `@app.step(gpu='A100')` to route to GPU workers when available
- Shape is always `[512, 512]` since size=512 produces a 512x512 matrix
