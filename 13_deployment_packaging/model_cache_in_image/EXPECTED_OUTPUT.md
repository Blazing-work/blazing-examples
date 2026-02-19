# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'model': 'weights'}
```

## Notes

- The image bakes `echo "weights" > /models/model.txt` at build time; the step reads that file
- `MODEL_PATH=/models/model.txt` is set via `image.env()` and read with `os.getenv()`
- Requires a running Blazing infrastructure: `docker-compose up -d`
