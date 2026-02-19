# OCR Job Queue

Async OCR processing with Redis-backed job state machine and HTTP polling.

## Patterns

- Submit → immediate job_id → background process → poll until complete
- Job state machine: `pending → processing → completed | failed`
- `asyncio.create_task()` — non-blocking background processing
- Redis for job state persistence across requests

## Setup

Requires `redis` connector and OpenAI API key.

## Endpoints

- `POST /ocr` — submit image (raw bytes body) → `{"job_id": "uuid"}`
- `GET /jobs/{job_id}` — poll status → `{"status": "completed", "result": "..."}`
