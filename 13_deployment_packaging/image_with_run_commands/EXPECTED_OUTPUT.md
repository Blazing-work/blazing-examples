# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'seed': 'seed'}
```

## Notes

- The `run_commands` bake `echo "seed" > /app/data/seed.txt` into the image at build time
- The step reads that file and returns its stripped content: `'seed'`
- Requires a running Blazing infrastructure: `docker-compose up -d`
