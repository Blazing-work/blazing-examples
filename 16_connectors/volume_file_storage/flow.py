"""
Volume File Storage with VolumeConnector

Read and write files through trusted services using LocalVolumeService and
VolumeConnector. Sandboxed steps cannot access volumes directly — only trusted
services with the VolumeConnector injected can perform file I/O, enforcing the
same security model as database and secrets connectors.

Patterns shown:
  1. LocalVolumeService — local emulator for dev/test with full Volume API
  2. VolumeConnector injected into FileProcessorService via connector_instances
  3. volume.put_file(path, bytes) + volume.commit() — write and flush
  4. volume.get_file(path) — read bytes
  5. volume.stat(path) — get file size and metadata
  6. FileProcessorService — trusted service: write_file, read_file, process_files
  7. LocalStack.create_volume() — stack-managed volume with persistence

Requires: pip install blazing
"""

import asyncio
import tempfile
from pathlib import Path

from blazing import LocalStack, LocalVolumeService, VolumeConnector, Volume
from blazing.base import BaseService


# ── FileProcessorService — trusted service, uses VolumeConnector for file I/O ─

class FileProcessorService(BaseService):
    """
    Trusted service that reads and writes files through a VolumeConnector.
    Sandboxed steps call service methods instead of accessing storage directly.
    """
    def __init__(self, connector_instances=None):
        self.connector_instances = connector_instances
        self.volume = connector_instances.get('storage') if connector_instances else None

    async def write_file(self, path: str, content: str) -> dict:
        """Write content to a file in the volume."""
        await self.volume.put_file(path, content.encode('utf-8'))
        # commit() flushes writes to durable storage — always call after writes
        # that must be visible to other workers
        await self.volume.commit()

        stat = await self.volume.stat(path)
        return {
            "path": path,
            "size": stat.size,
            "written": True,
        }

    async def read_file(self, path: str) -> dict:
        """Read content from a file in the volume."""
        try:
            data = await self.volume.get_file(path)
            return {
                "path": path,
                "content": data.decode('utf-8'),
                "found": True,
            }
        except FileNotFoundError:
            return {"path": path, "found": False}

    async def process_files(self, input_path: str, output_path: str) -> dict:
        """Read input, uppercase, write to output — typical transform pattern."""
        input_data = await self.volume.get_file(input_path)
        content = input_data.decode('utf-8')

        # Transform: uppercase
        transformed = content.upper()

        await self.volume.put_file(output_path, transformed.encode('utf-8'))
        await self.volume.commit()

        return {
            "input_path": input_path,
            "output_path": output_path,
            "input_size": len(content),
            "output_size": len(transformed),
        }


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    print("=== Volume File Storage with VolumeConnector ===")
    print()

    with tempfile.TemporaryDirectory(prefix="blazing-volume-") as tmp:
        storage_path = Path(tmp)

        # ── Pattern 1: LocalVolumeService standalone — write and read ──────────
        print("--- Pattern 1: FileProcessorService with VolumeConnector ---")
        vol_svc = LocalVolumeService(storage_path=str(storage_path / "volumes"))
        await vol_svc.start()

        vol = await vol_svc.create_volume("app-data")
        service = FileProcessorService({'storage': vol})

        write_result = await service.write_file("/hello.txt", "Hello, Blazing!")
        print(f"  Written: {write_result['path']} ({write_result['size']} bytes)")

        read_result = await service.read_file("/hello.txt")
        print(f"  Read back: {read_result['content']!r}")

        # ── Pattern 2: process_files — read → transform → write ──────────────
        print()
        print("--- Pattern 2: Transform pipeline (uppercase) ---")
        await vol.put_file("/input/data.txt", b"hello world from blazing")
        await vol.commit()

        proc_result = await service.process_files("/input/data.txt", "/output/result.txt")
        print(f"  Input:  {proc_result['input_path']} ({proc_result['input_size']} bytes)")
        print(f"  Output: {proc_result['output_path']} ({proc_result['output_size']} bytes)")

        output_data = await vol.get_file("/output/result.txt")
        print(f"  Transformed: {output_data.decode()!r}")

        # ── Pattern 3: LocalStack.create_volume — stack-managed volume ─────────
        print()
        print("--- Pattern 3: LocalStack-managed volume with multi-worker reload ---")
        stack = LocalStack(storage_path=str(storage_path / "stack"))
        await stack.start(start_registry_server=False)

        pipeline_vol = await stack.create_volume("pipeline-vol")
        await pipeline_vol.put_file("/worker1/result.json", b'{"status": "done", "items": 42}')
        await pipeline_vol.commit()

        # Simulate a second worker: get a fresh volume handle, reload to see writes
        pipeline_vol2 = await stack.create_volume("pipeline-vol")
        await pipeline_vol2.reload()  # reload() syncs local cache with durable storage

        data = await pipeline_vol2.get_file("/worker1/result.json")
        print(f"  Worker 2 read Worker 1 data: {data.decode()}")

        # Worker 2 writes, Worker 1 reloads
        await pipeline_vol2.put_file("/worker2/result.json", b'{"status": "also done"}')
        await pipeline_vol2.commit()

        await pipeline_vol.reload()
        dirs = await pipeline_vol.listdir("/")
        print(f"  Root dirs after reload: {sorted(dirs)}")

        stats = stack.get_stats()
        print(f"  Stack volume count: {stats['volumes']['total_volumes']}")

        await stack.stop()
        await vol_svc.stop()

    print()
    print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
