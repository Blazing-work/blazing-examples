"""
S3 connector tests — real object storage operations.

Validates upload/download roundtrip, listing, deletion, presigned URLs,
and large file transfer against MinIO or AWS S3.

Run (MinIO via Docker):
    docker run -p 9000:9000 minio/minio server /data
    S3_ENDPOINT_URL=http://localhost:9000 pytest 15_connector_tests/s3/ -v

Run (AWS S3):
    AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... \
    S3_ENDPOINT_URL=https://s3.amazonaws.com \
    S3_TEST_BUCKET=my-bucket pytest 15_connector_tests/s3/ -v
"""

import os
import uuid
import pytest
import pytest_asyncio
import httpx

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("S3_ENDPOINT_URL"), reason="S3_ENDPOINT_URL not set"),
]


@pytest_asyncio.fixture
async def prefix(s3_connector, s3_test_bucket, unique_id):
    """Unique key prefix; cleans up all objects after the test."""
    p = f"e2e-test/{unique_id}/"
    yield p
    try:
        objects = await s3_connector.list_objects(bucket=s3_test_bucket, prefix=p)
        for obj in objects:
            await s3_connector.delete(bucket=s3_test_bucket, key=obj["key"])
    except Exception:
        pass


@pytest.mark.timeout(30)
async def test_upload_download_roundtrip(s3_connector, s3_test_bucket, prefix):
    """Upload bytes and download them back byte-for-byte."""
    content = b"Hello E2E roundtrip"
    key = prefix + "test.txt"
    await s3_connector.upload(bucket=s3_test_bucket, key=key, data=content)
    assert await s3_connector.download(bucket=s3_test_bucket, key=key) == content


@pytest.mark.timeout(30)
async def test_list_objects(s3_connector, s3_test_bucket, prefix):
    """Upload 3 objects and verify all 3 appear in list."""
    for name in ["a.txt", "b.txt", "c.txt"]:
        await s3_connector.upload(bucket=s3_test_bucket, key=prefix + name, data=name.encode())

    objects = await s3_connector.list_objects(bucket=s3_test_bucket, prefix=prefix)
    assert len(objects) == 3
    keys = {obj["key"] for obj in objects}
    assert {prefix + n for n in ["a.txt", "b.txt", "c.txt"]} == keys


@pytest.mark.timeout(30)
async def test_delete_object(s3_connector, s3_test_bucket, prefix):
    """Delete an object and confirm download raises an exception."""
    key = prefix + "delete-me.txt"
    await s3_connector.upload(bucket=s3_test_bucket, key=key, data=b"bye")
    await s3_connector.delete(bucket=s3_test_bucket, key=key)
    with pytest.raises(Exception):
        await s3_connector.download(bucket=s3_test_bucket, key=key)


@pytest.mark.timeout(30)
async def test_presigned_url(s3_connector, s3_test_bucket, prefix):
    """Presigned URL is accessible via HTTP and returns the original content."""
    content = b"presigned content"
    key = prefix + "presigned.txt"
    await s3_connector.upload(bucket=s3_test_bucket, key=key, data=content)

    url = await s3_connector.presign_url(bucket=s3_test_bucket, key=key, expiration=300)
    assert url.startswith("http")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        assert resp.status_code == 200
        assert resp.content == content


@pytest.mark.timeout(30)
async def test_large_file(s3_connector, s3_test_bucket, prefix):
    """Upload and download a 1 MB file."""
    content = b"x" * 1024 * 1024
    key = prefix + "large.bin"
    await s3_connector.upload(bucket=s3_test_bucket, key=key, data=content)
    downloaded = await s3_connector.download(bucket=s3_test_bucket, key=key)
    assert len(downloaded) == 1024 * 1024
