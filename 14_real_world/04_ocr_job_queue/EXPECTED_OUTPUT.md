# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `OPENAI_API_KEY` for GPT-4o Vision OCR
- Redis for job state persistence (via RedisDictConnector)
- Running Blazing infrastructure: `docker-compose up -d`

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - OCRJobService - Job {uuid} created: status=pending
INFO - OCRJobService - Processing job {uuid}
INFO - OCRJobService - Job {uuid} completed: 142 characters extracted
{"job_id": "{uuid}", "status": "completed", "text": "Invoice #1234\nDate: 2024-01-15\nAmount: $99.99"}
```

## Notes

- `job_id` is a UUID generated at job creation — it will differ on each run
- The extracted OCR text depends on the image submitted
- API costs apply for each GPT-4o Vision call (image tokens vary by image size)
- Clients poll `GET /jobs/{job_id}` until `status` is `completed` or `failed`
