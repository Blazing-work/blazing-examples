# mongoDB

MongoDB is a document-oriented NoSQL database designed for high performance, high availability, and easy scalability.

## Use Cases

- Content management systems
- Real-time analytics
- IoT data storage
- Mobile app backends
- Catalog and inventory management

## Getting Started

1. Wait for the "Waiting for connections" log message
2. Connect with `mongosh` or a MongoDB driver
3. Create collections and insert documents to get started

## Accessing the Service

Connect using the Mongo shell:
```bash
mongosh --host {SERVICE_URI} --port 27017
```


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `MONGO_INITDB_ROOT_USERNAME` | `root` |

### Secrets

The following values are configured as secrets and should be set securely:

- `MONGO_INITDB_ROOT_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `mongo:latest` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 27017 |

## Documentation

For full documentation, visit: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
