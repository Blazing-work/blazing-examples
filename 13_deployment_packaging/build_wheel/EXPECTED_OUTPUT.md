# Expected Output

## Running

```bash
python flow.py
```

## Output

```
{'wheel': 'mypackage-0.1.0-py3-none-any.whl'}
```

## Notes

- The wheel filename reflects the package name and version in your `setup.py` or `pyproject.toml`
- The exact filename will vary based on the package configuration in the current directory
- Requires the current directory to contain a valid Python package (`setup.py` or `pyproject.toml`)
