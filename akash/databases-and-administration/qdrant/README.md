## What is Qdrant?

Qdrant is a high-performance vector similarity search engine and database. It's designed for machine learning applications requiring efficient vector search capabilities, including:
- Semantic search
- Recommendation systems
- Neural network applications
- Image/video similarity search
- Embeddings storage and retrieval

## Accessing Qdrant

Once deployed, you'll receive a URI in the format:

### Health Check

```bash
curl http://<your-uri>/
```

### Web UI

Access the Qdrant dashboard at:
```
http://<your-uri>/dashboard
```


### Adjust Resources

Edit the `profiles.compute.qdrant.resources` section:

```yaml
resources:
  cpu:
    units: 4  # Increase for better performance
  memory:
    size: 8Gi  # Increase for larger datasets
  storage:
    - size: 10Gi
    - name: data
      size: 100Gi  # Increase for more vector data
```

## Resources

- [Qdrant Documentation](https://qdrant.tech/documentation/)

- [Qdrant GitHub](https://github.com/qdrant/qdrant)
