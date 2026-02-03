# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Importing CSV file...
[Simulated] Created user: John Doe (john@example.com) -> ID: XXXX
[Simulated] Created user: Jane Smith (jane@example.com) -> ID: XXXX
[Simulated] Created user: Alice Brown (alice@example.com) -> ID: XXXX

CSV Import completed!
  File: users/import.csv
  Total rows: 4
  Imported: 3
  Errors: 1
```

## Notes

- User IDs (XXXX) are randomly generated between 1000-9999 and will vary each run
- Simulated CSV contains 4 rows, but Bob Wilson has missing email so only 3 are imported
- One validation error is reported (Bob Wilson's missing email)
- In production, would use actual file storage and database services
- Order of user creation messages may vary
