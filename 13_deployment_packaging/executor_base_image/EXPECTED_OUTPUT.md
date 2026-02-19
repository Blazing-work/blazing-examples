# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'mean': 2.5}
```

## Notes

- `mean([1, 2, 3, 4]) = 2.5` — computed by numpy inside the executor base image
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The image extends `Image.executor()` with apt packages, pip packages, and environment variables
