# Expected Output

## Running

```bash
python flow.py
```

## Output

```
Generating daily report for 2024-01-15...
  [EMAIL] Sent to ceo@example.com: Daily Report
  [EMAIL] Sent to cfo@example.com: Daily Report
  [EMAIL] Sent to analytics@example.com: Daily Report

Report generated and sent to 3 recipients

--- Generated Report ---

Daily Report - 2024-01-15
================================
Total Orders: 1,523
Revenue: $45,678.90
Active Users: 892
```

## Notes

- Fetches metrics from simulated database for January 15, 2024
- Generates formatted report with metrics
- Sends report to 3 recipients concurrently (parallel email sending)
- Output order of email sending may vary due to parallel execution
- Uses simulated services (MetricsDatabase, EmailService, ConfigService)
- Demonstrates scheduled reporting workflow with data aggregation and distribution
