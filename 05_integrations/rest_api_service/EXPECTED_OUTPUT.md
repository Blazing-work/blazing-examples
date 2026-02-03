# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Checking weather for New York...
[API] Fetching weather for New York...
  Temperature: 72°F
  Conditions: Sunny

Checking weather for London...
[API] Fetching weather for London...
  Temperature: 58°F
  Conditions: Cloudy

Checking weather for Tokyo...
[API] Fetching weather for Tokyo...
  Temperature: 68°F
  Conditions: Partly Cloudy
```

## Notes

- Fetches weather for 3 cities sequentially: New York, London, and Tokyo
- Uses simulated weather data (not real API calls)
- WeatherAPI is implemented as a BaseService with @app.service decorator
- In production, would use actual REST API with httpx and API keys
- Demonstrates REST API service integration pattern with service injection
