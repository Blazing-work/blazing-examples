# elasticsearch

[Elasticsearch](https://github.com/elastic/elasticsearch) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene.
[Kibana](https://github.com/elastic/kibana) is a source-available data visualization dashboard software for Elasticsearch.
Check the status of your deployment using [REST API](https://www.elastic.co/docs/reference/elasticsearch/rest-apis) requests. For example:

## Use Cases

- Full-text search
- Privacy-respecting search
- Data indexing

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:9200/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:9200/` in your browser or send HTTP requests to this address.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `discovery.type` | `single-node` |
| `http.host` | `0.0.0.0` |
| `xpack.security.enabled` | `false` |
| `ES_JAVA_OPTS` | `-Xms4g -Xmx4g` |

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `elasticsearch:9.2.0` |
| CPU | 2.0 |
| Memory | 8gb |
| Storage | 32gb |
| Exposed Ports | 9200 |
