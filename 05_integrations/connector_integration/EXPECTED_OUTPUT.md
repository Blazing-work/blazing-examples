# Expected Output

## Running

```bash
python flow.py
```

## Output

```
============================================================
Connector Integration Patterns Demo
============================================================

1. Connector Configurations
----------------------------------------
  REST: MarketAPI -> https://api.marketdata.example.com
    Throttle: 10 req/1s
  SQL:  Database -> localhost:5432/market_data

2. Creating Connectors
----------------------------------------

3. Initializing Service
----------------------------------------
  [Connector] MarketAPI: Connected to https://api.marketdata.example.com
  [Connector] Database: Connected to localhost:5432/market_data

4. Health Check
----------------------------------------
  MarketAPI: OK
  Database: OK

5. Fetch Stock Data
----------------------------------------
  Fetched 1 stocks: [{'symbol': 'AAPL', 'price': 150.0}]

6. Fetch and Store Operation
----------------------------------------
  Success: True
  Data: {'symbol': 'AAPL', 'price': 150.0, 'change': 2.5}
  Records inserted: 1

7. Cleanup
----------------------------------------
  [Connector] MarketAPI: Disconnected
  [Connector] Database: Disconnected

============================================================
Key Patterns:
============================================================
  1. Connectors encapsulate external service access
  2. Services receive connector_instances dict
  3. Services use connectors via self.connector_instances['name']
  4. Health checks verify all connector connectivity
  5. Multiple connectors can be used in single operations
```

## Notes

- Uses simulated connectors for demonstration (production uses blazing.RESTConnector and blazing.SQLAlchemyConnector)
- Demonstrates connector lifecycle: configuration → connection → usage → cleanup
- Shows health checks for multiple connectors
- Illustrates fetching from REST API and storing in database using connectors
- Updated example from plan 04-04 to use current SDK patterns
