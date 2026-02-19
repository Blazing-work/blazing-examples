# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'result': 'hello'}
```

## Notes

- The echo step returns the message as-is: `run(message='hello') = 'hello'`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- The workflow uses `Image.from_dockerfile()` — the image is built from the Dockerfile in the current directory on first run
