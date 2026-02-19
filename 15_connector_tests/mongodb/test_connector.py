"""
MongoDB connector tests — real database operations.

Validates CRUD, bulk insert, aggregation pipelines, and projection+sort
against a live MongoDB instance (Atlas M0 free tier or local Docker).

Run:
    MONGODB_TEST_URI=mongodb+srv://... pytest 15_connector_tests/mongodb/ -v
"""

import os
import pytest

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not os.getenv("MONGODB_TEST_URI"), reason="MONGODB_TEST_URI not set"),
]


@pytest.mark.timeout(30)
async def test_insert_and_find(mongodb_connector, unique_id):
    """Insert a document and find it by filter."""
    coll = f"e2e_{unique_id}"
    try:
        doc_id = await mongodb_connector.insert(coll, {"name": "e2e", "value": 42, "tags": ["a", "b"]})
        assert isinstance(doc_id, str)

        results = await mongodb_connector.find(collection=coll, filter={"name": "e2e"}, limit=1)
        assert len(results) == 1
        assert results[0]["value"] == 42
        assert results[0]["tags"] == ["a", "b"]
    finally:
        await (await mongodb_connector._get_collection(coll)).drop()


@pytest.mark.timeout(30)
async def test_update_and_delete(mongodb_connector, unique_id):
    """Update a field then delete the document."""
    coll = f"e2e_{unique_id}"
    try:
        await mongodb_connector.insert(coll, {"name": "update_me", "count": 1})

        modified = await mongodb_connector.update(
            collection=coll, filter={"name": "update_me"}, update={"$set": {"count": 5}}
        )
        assert modified == 1

        results = await mongodb_connector.find(collection=coll, filter={"name": "update_me"}, limit=1)
        assert results[0]["count"] == 5

        deleted = await mongodb_connector.delete(collection=coll, filter={"name": "update_me"})
        assert deleted == 1

        results = await mongodb_connector.find(collection=coll, filter={"name": "update_me"}, limit=1)
        assert len(results) == 0
    finally:
        await (await mongodb_connector._get_collection(coll)).drop()


@pytest.mark.timeout(30)
async def test_bulk_insert_and_count(mongodb_connector, unique_id):
    """Bulk-insert 50 documents and verify the count."""
    coll = f"e2e_{unique_id}"
    try:
        docs = [{"index": i, "batch": "e2e"} for i in range(50)]
        count = await mongodb_connector.bulk_insert(collection=coll, documents=docs)
        assert count == 50

        results = await mongodb_connector.find(collection=coll, filter={"batch": "e2e"}, limit=100)
        assert len(results) == 50
    finally:
        await (await mongodb_connector._get_collection(coll)).drop()


@pytest.mark.timeout(30)
async def test_aggregation_pipeline(mongodb_connector, unique_id):
    """Group by category with $sum aggregation."""
    coll = f"e2e_{unique_id}"
    try:
        docs = [{"category": "A", "amount": 10}] * 5 + [{"category": "B", "amount": 20}] * 5
        await mongodb_connector.bulk_insert(collection=coll, documents=docs)

        results = await mongodb_connector.aggregate(
            collection=coll,
            pipeline=[{"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}],
        )
        totals = {r["_id"]: r["total"] for r in results}
        assert totals["A"] == 50
        assert totals["B"] == 100
    finally:
        await (await mongodb_connector._get_collection(coll)).drop()


@pytest.mark.timeout(30)
async def test_find_with_projection_and_sort(mongodb_connector, unique_id):
    """Projection excludes fields; sort orders results correctly."""
    coll = f"e2e_{unique_id}"
    try:
        await mongodb_connector.bulk_insert(collection=coll, documents=[
            {"name": "first", "priority": 5, "extra": "x"},
            {"name": "second", "priority": 3, "extra": "x"},
            {"name": "third", "priority": 8, "extra": "x"},
        ])
        results = await mongodb_connector.find(
            collection=coll,
            filter={},
            projection={"name": 1, "_id": 0},
            sort=[("priority", -1)],
            limit=10,
        )
        names = [r["name"] for r in results]
        assert names == ["third", "first", "second"]
        for doc in results:
            assert "extra" not in doc
            assert "_id" not in doc
    finally:
        await (await mongodb_connector._get_collection(coll)).drop()
