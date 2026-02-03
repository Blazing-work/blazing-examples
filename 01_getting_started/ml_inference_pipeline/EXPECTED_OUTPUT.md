# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Inference results: [{'id': '1', 'prediction': 'label_value', 'confidence': 0.XX, 'metadata': {}}, {'id': '2', 'prediction': 'label_value', 'confidence': 0.XX, 'metadata': {}}]
```

## Notes

- Requires MODEL_ENDPOINT environment variable to be set (defaults to "http://model-server:8080")
- Actual output depends on the model server's response
- Example shows structure with simulated values
- Prediction labels and confidence scores will vary based on model output
- BATCH_SIZE environment variable controls batching (default: 32)
- Without a running model server, this will fail with connection error
- Preprocesses data → batches inference calls → postprocesses results
- Sample data includes two items with normalized features
