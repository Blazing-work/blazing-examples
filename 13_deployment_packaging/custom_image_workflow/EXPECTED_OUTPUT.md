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

- `mean([1, 2, 3, 4]) = 2.5` — computed by numpy inside the custom Docker image
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The workflow uses `Image.debian_slim(python_version='3.11').pip_install('numpy')` — the image is built on first run
