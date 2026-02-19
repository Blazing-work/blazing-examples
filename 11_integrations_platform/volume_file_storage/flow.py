"""
Volume File Storage Example for Blazing

Volumes provide persistent file storage for services. They survive across
workflow executions and are shared between workers of the same service.

Key concepts:
  - Volume.persisted("name")   — durable storage (survives restarts)
  - Volume.ephemeral("name")   — temporary storage (cleared on restart)
  - VolumeConnector            — injected into services, provides file I/O
  - Volumes are ONLY accessible through Services (not directly in sandboxed Steps)
    — same security model as databases

Patterns shown:
  1. Writing and reading files via VolumeConnector
  2. ML checkpoint saving and loading
  3. Data pipeline: read input, transform, write output

Requires: docker-compose up -d
"""

import os

from blazing import Blazing, BaseService
from blazing.volumes import Volume

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)

# Declare volumes at module level — reference by name across services and deployments
model_storage = Volume.persisted("model-checkpoints")
scratch_storage = Volume.ephemeral("pipeline-scratch")


# ── Pattern 1: File Processor Service ─────────────────────────────────────────

@app.service(volumes=[model_storage])
class CheckpointService(BaseService):
    """
    Service that saves and loads model checkpoints.

    VolumeConnector is injected by Blazing at runtime.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.volume = (connector_instances or {}).get("model-checkpoints")

    async def save_checkpoint(self, epoch: int, weights: bytes) -> dict:
        """Save model weights for a training epoch."""
        path = f"/checkpoints/epoch_{epoch:04d}.bin"
        await self.volume.put_file(path, weights)
        await self.volume.commit()

        stat = await self.volume.stat(path)
        return {"path": path, "size": stat.size, "epoch": epoch}

    async def load_checkpoint(self, epoch: int) -> bytes:
        """Load model weights for a specific epoch."""
        path = f"/checkpoints/epoch_{epoch:04d}.bin"
        return await self.volume.get_file(path)

    async def list_checkpoints(self) -> list:
        """List all saved checkpoints."""
        try:
            files = await self.volume.listdir("/checkpoints")
            return sorted(files)
        except FileNotFoundError:
            return []

    async def latest_epoch(self) -> int:
        """Return the index of the latest saved checkpoint, or -1 if none."""
        checkpoints = await self.list_checkpoints()
        if not checkpoints:
            return -1
        last = checkpoints[-1]  # e.g. "epoch_0003.bin"
        return int(last.split("_")[1].split(".")[0])


# ── Pattern 2: Data Pipeline Service ─────────────────────────────────────────

@app.service(volumes=[scratch_storage])
class PipelineService(BaseService):
    """
    Service that stages intermediate data in a scratch volume.

    Use ephemeral volumes for intermediate files that don't need to
    survive a service restart.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.volume = (connector_instances or {}).get("pipeline-scratch")

    async def stage_input(self, job_id: str, data: bytes) -> str:
        """Write raw input to scratch storage for later steps."""
        path = f"/jobs/{job_id}/input.bin"
        await self.volume.put_file(path, data)
        await self.volume.commit()
        return path

    async def read_staged(self, path: str) -> bytes:
        """Read staged file from scratch storage."""
        return await self.volume.get_file(path)

    async def cleanup_job(self, job_id: str) -> int:
        """Remove all files for a completed job. Returns file count deleted."""
        try:
            files = await self.volume.listdir(f"/jobs/{job_id}")
        except FileNotFoundError:
            return 0
        for f in files:
            await self.volume.delete_file(f"/jobs/{job_id}/{f}")
        await self.volume.commit()
        return len(files)


# ── Workflow ──────────────────────────────────────────────────────────────────

@app.workflow
async def training_loop(num_epochs: int = 3, services=None) -> dict:
    """Simulate a training loop that checkpoints each epoch."""
    svc = services.get("CheckpointService")
    start_epoch = await svc.latest_epoch() + 1

    saved = []
    for epoch in range(start_epoch, start_epoch + num_epochs):
        # In production: actual training happens in @app.step
        fake_weights = f"weights_epoch_{epoch}".encode()
        result = await svc.save_checkpoint(epoch, fake_weights)
        saved.append(result)

    checkpoints = await svc.list_checkpoints()
    return {"epochs_saved": len(saved), "total_checkpoints": len(checkpoints), "details": saved}


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("Volume File Storage Patterns:")
    print()
    print("  Volume.persisted('name')  — durable storage")
    print("  Volume.ephemeral('name')  — temporary, cleared on restart")
    print()
    print("  @app.service(volumes=[vol]) — declares which volumes a service uses")
    print("  connector_instances['vol-name'] — VolumeConnector injected at runtime")
    print()
    print("  volume.put_file(path, bytes)  — write file")
    print("  volume.get_file(path)         — read file")
    print("  volume.listdir(path)          — list directory")
    print("  volume.commit()               — flush writes to durable storage")
    print()

    await app.publish()
    result = await app.run(training_loop, args=(3,))
    print(f"Training result: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
