# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'FOO': 'bar'}
```

## Notes

- The step reads the `FOO` environment variable baked into the image: `Image.executor().env(FOO='bar')`
- Requires a running Blazing infrastructure: `docker-compose up -d`
- Demonstrates how to embed environment variables into a custom executor image
