"""
OCR Job Queue Example for Blazing

Demonstrates asynchronous job processing with status polling using:
- UUID-based job IDs
- Redis job state persistence via RedisDictConnector
- OpenAI Vision API (gpt-4o) for OCR
- Job state machine: pending → processing → completed|failed
- Non-blocking workflow execution
- HTTP status polling
"""

import os
import logging
import uuid
import base64
from datetime import datetime
from typing import Dict, Any

from blazing import Blazing, BaseService
from blazing_service.connectors.openai import OpenAIConnector
from blazing_service.connectors.secrets import SecretsConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=["api.openai.com"])
class OCRJobService(BaseService):
    """
    OCR Job service with async processing and status polling.

    Workflow:
    1. Client POSTs image to /ocr → receives job_id immediately
    2. Service stores job state in Redis (status: pending)
    3. Service triggers async workflow (non-blocking)
    4. Client polls GET /jobs/{job_id} until status is completed or failed
    5. Workflow updates job state: pending → processing → completed|failed
    """

    def __init__(self, connector_instances=None):
        """Initialize OCR job service with OpenAI and Redis."""
        super().__init__(connector_instances)

        self.secrets = connector_instances.get('secrets') if connector_instances else SecretsConnector()
        self.redis = connector_instances.get('redis') if connector_instances else None
        self.openai = connector_instances.get('openai') if connector_instances else None

        if self.redis is None:
            raise ValueError("RedisDictConnector is required for OCRJobService. Configure 'redis' connector.")

        logger.info("OCRJobService initialized with Redis for job state persistence")

    async def _ensure_openai_connected(self):
        """Ensure OpenAI connector is initialized and connected."""
        if self.openai is None:
            api_key = await self.secrets.get("OPENAI_API_KEY")
            self.openai = OpenAIConnector(api_key=api_key)

        if not self.openai.is_connected:
            await self.openai.connect()

    async def submit_job(self, image_data: bytes) -> str:
        """
        Submit OCR job and return job ID immediately.

        Job state is initialized in Redis as 'pending', then an async
        workflow is triggered to process the OCR in the background.

        Returns:
            Job ID (UUID string)
        """
        job_id = str(uuid.uuid4())

        await self.redis.set(f"job:{job_id}", {
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "image_size": len(image_data)
        })

        logger.info(f"Job {job_id} created with status 'pending'")

        # Store image data in Redis for workflow to access
        await self.redis.set(f"job:{job_id}:image", base64.b64encode(image_data).decode())

        return job_id

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get current job status from Redis.

        Returns:
            Job state dictionary with status, timestamps, result/error

        Raises:
            ValueError: If job not found
        """
        job_data = await self.redis.get(f"job:{job_id}")

        if not job_data:
            raise ValueError(f"Job {job_id} not found")

        return job_data

    async def process_ocr(self, job_id: str):
        """
        Process OCR job: extract text from image using OpenAI Vision API.

        Updates job state through the state machine:
        pending → processing → completed (or failed)
        """
        await self._ensure_openai_connected()

        # Update to processing
        job_data = await self.redis.get(f"job:{job_id}")
        job_data["status"] = "processing"
        job_data["started_at"] = datetime.utcnow().isoformat()
        await self.redis.set(f"job:{job_id}", job_data)

        logger.info(f"Job {job_id} status updated to 'processing'")

        try:
            base64_image = await self.redis.get(f"job:{job_id}:image")

            if not base64_image:
                raise ValueError("Image data not found in Redis")

            # gpt-4o supports vision (gpt-4o-mini does NOT)
            response = await self.openai.chat(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all text from this image. Return only the text, no commentary."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                model="gpt-4o",
                max_tokens=1000
            )

            extracted_text = response['choices'][0]['message']['content']

            job_data["status"] = "completed"
            job_data["completed_at"] = datetime.utcnow().isoformat()
            job_data["result"] = extracted_text
            await self.redis.set(f"job:{job_id}", job_data)

            await self.redis.delete(f"job:{job_id}:image")

            logger.info(f"Job {job_id} completed successfully")

        except Exception as e:
            job_data = await self.redis.get(f"job:{job_id}")
            job_data["status"] = "failed"
            job_data["failed_at"] = datetime.utcnow().isoformat()
            job_data["error"] = str(e)
            await self.redis.set(f"job:{job_id}", job_data)

            logger.error(f"Job {job_id} failed: {e}")


@app.endpoint.post("/ocr")
async def submit_ocr(request, services=None):
    """
    Submit OCR job.

    Expects raw image bytes in request body.

    Returns:
        JSON: {"job_id": "uuid-string"}
    """
    import asyncio

    image_data = await request.body()

    if not image_data:
        return {"error": "No image data provided"}, 400

    ocr_service = services['OCRJobService']
    job_id = await ocr_service.submit_job(image_data)

    # Trigger processing in background (non-blocking)
    asyncio.create_task(ocr_service.process_ocr(job_id))

    return {"job_id": job_id}


@app.endpoint.get("/jobs/{job_id}")
async def get_job_status(request, services=None):
    """
    Poll job status.

    Returns:
        JSON with job state:
        {
            "status": "pending|processing|completed|failed",
            "created_at": "ISO timestamp",
            "started_at": "ISO timestamp" (if processing/completed/failed),
            "completed_at": "ISO timestamp" (if completed),
            "result": "extracted text" (if completed),
            "error": "error message" (if failed)
        }
    """
    job_id = request.path_params['job_id']
    ocr_service = services['OCRJobService']

    try:
        job_data = await ocr_service.get_job_status(job_id)
        return job_data
    except ValueError as e:
        return {"error": str(e)}, 404


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
