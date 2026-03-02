# Neo4j


This guide helps you deploy a Neo4j graph database  decentralized cloud network with persistent storage.

## Overview

Neo4j is a powerful graph database that stores data as nodes and relationships. This deployment provides:

- Neo4j 5.15.0 (latest stable version)
- Browser interface (port 7474)
- Bolt protocol access (port 7687)
- Persistent storage for data and logs
- Optimized memory configuration


### 1. Update Security Settings


```yaml
- NEO4J_AUTH=neo4j/your-secure-password-here
```

Replace `your-secure-password-here` with a strong password.

### 2. Adjust Resources (Optional)

Modify the compute resources based on your needs:

```yaml
cpu:
  units: 2           # CPU cores
memory:
  size: 4Gi          # RAM
storage:
  - size: 10Gi       # Database storage
  - size: 5Gi        # Logs storage
```

### 3. Update Pricing

Check current Blazing Core market rates and adjust the bid price:

```yaml
pricing:
  neo4j:
    amount: 1000     # Adjust based on current market rates
```


### Browser Interface

Once deployed, access the Neo4j Browser at:

```
http://<provider-uri>:7474
```

Login with:
- **Username:** neo4j

### Bolt Connection

Connect your applications using the Bolt protocol:

```
bolt://<provider-uri>:7687
```

## Persistent Storage

This deployment uses Blazing Core's persistent storage feature:

- **Data Volume:** 10 GB mounted at `/data` (database files)
- **Logs Volume:** 5 GB mounted at `/logs` (log files)
- **Storage Class:** beta3

Your data will persist across:
- Container restarts
- Pod rescheduling
- Redeployments to the same provider

**Important:** Persistent storage requires providers with storage support enabled.

## Resources


- [Neo4j Documentation](https://neo4j.com/docs/)

- [Neo4j Community](https://community.neo4j.com/)
