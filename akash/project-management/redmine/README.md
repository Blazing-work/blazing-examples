# redmine

MySQL is the world's most popular open-source relational database management system.

## Use Cases

- Web application backends
- Content management systems
- E-commerce platforms
- Data-driven applications

## Getting Started

1. Wait for initialization to complete (check logs for "ready for connections")
2. Connect with the MySQL client or your application
3. Create databases and grant permissions as needed

## Accessing the Service

Connect using the MySQL CLI:
```bash
mysql -h {SERVICE_URI} -P 3306 -u root -p
```

### Default Credentials

- **Username**: `root`
- **Password**: Set via `MYSQL_ROOT_PASSWORD`

## Configuration

- `MYSQL_DATABASE` creates a database on first start
- `MYSQL_USER` / `MYSQL_PASSWORD` create an additional user

### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `MYSQL_DATABASE` | `redmine` |
| `REDMINE_DB_MYSQL` | `db` |
| `REDMINE_DB_USERNAME` | `root` |

### Secrets

The following values are configured as secrets and should be set securely:

- `MYSQL_ROOT_PASSWORD`
- `REDMINE_DB_PASSWORD`


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `mysql:5.7` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 3306 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `redmine` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 3000 |

## Documentation

For full documentation, visit: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
