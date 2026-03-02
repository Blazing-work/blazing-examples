# couchdb

Apache CouchDB is a document-oriented NoSQL database with a RESTful HTTP API, built for reliability and data sync.

## Use Cases

- Offline-first applications
- Document storage with replication
- RESTful data APIs
- Multi-device sync

## Getting Started

1. Open Fauxton at `/_utils/` to manage databases visually
2. Create a database: `PUT http://{URI}:{PORT}/mydb`
3. Insert documents via the REST API or Fauxton

## Accessing the Service

Access the Fauxton web UI at `http://{SERVICE_URI}:5984/_utils/` or use the HTTP API directly:
```bash
curl http://{SERVICE_URI}:5984/
```

### Default Credentials

- **Username**: `admin`
- **Password**: Set via `COUCHDB_USER` / `COUCHDB_PASSWORD`


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `COUCHDB_USER` | `admin` |

### Secrets

The following values are configured as secrets and should be set securely:

- `COUCHDB_PASSWORD`

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `couchdb` |
| CPU | 1.0 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 5984 |

## Documentation

For full documentation, visit: [https://docs.couchdb.org/](https://docs.couchdb.org/)
