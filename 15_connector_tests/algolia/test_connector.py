"""
Algolia connector tests — real search API operations.

Validates indexing, searching, deletion, and filtering against a live
Algolia account. Each test creates a unique index and cleans it up.

Run:
    ALGOLIA_APP_ID=... ALGOLIA_API_KEY=... pytest 15_connector_tests/algolia/ -v
"""

import os
import uuid
import pytest
import pytest_asyncio

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(
        not os.getenv("ALGOLIA_APP_ID") or not os.getenv("ALGOLIA_API_KEY"),
        reason="ALGOLIA_APP_ID or ALGOLIA_API_KEY not set",
    ),
]


@pytest_asyncio.fixture
async def test_index(algolia_connector):
    index_name = f"e2e_{uuid.uuid4().hex[:12]}"
    yield index_name
    try:
        await algolia_connector.delete_index(index_name)
    except Exception:
        pass


@pytest.mark.timeout(30)
async def test_index_and_search(algolia_connector, test_index):
    """Index one record and find it via search."""
    record = {"objectID": "test-1", "title": "E2E Test Object", "content": "Blazing integration test"}
    result = await algolia_connector.index_record(record=record, index_name=test_index)
    assert result["objectID"] == "test-1"
    await algolia_connector.wait_for_task(test_index, result["taskID"])

    hits = await algolia_connector.search(query="E2E Test", index_name=test_index)
    assert hits["nb_hits"] >= 1
    found = [h for h in hits["hits"] if h["objectID"] == "test-1"]
    assert len(found) == 1
    assert found[0]["title"] == "E2E Test Object"


@pytest.mark.timeout(30)
async def test_batch_index(algolia_connector, test_index):
    """Batch-index 10 records and verify all are searchable."""
    records = [{"objectID": f"batch-{i}", "name": f"Item {i}", "value": i} for i in range(10)]
    result = await algolia_connector.batch_index(records=records, index_name=test_index, wait=True)
    assert result["count"] == 10

    hits = await algolia_connector.search(query="Item", index_name=test_index, hits_per_page=20)
    assert hits["nb_hits"] >= 10


@pytest.mark.timeout(30)
async def test_delete_record(algolia_connector, test_index):
    """Delete a record and confirm it no longer appears in search."""
    record = {"objectID": "delete-me", "title": "Will be deleted"}
    index_result = await algolia_connector.index_record(record=record, index_name=test_index)
    await algolia_connector.wait_for_task(test_index, index_result["taskID"])

    delete_result = await algolia_connector.delete_record(object_id="delete-me", index_name=test_index)
    await algolia_connector.wait_for_task(test_index, delete_result["taskID"])

    hits = await algolia_connector.search(query="Will be deleted", index_name=test_index)
    assert hits["nb_hits"] == 0


@pytest.mark.timeout(10)
async def test_objectid_validation(algolia_connector, test_index):
    """Client-side validation rejects records missing objectID."""
    with pytest.raises(ValueError, match="objectID"):
        await algolia_connector.index_record(record={"title": "No objectID"}, index_name=test_index)


@pytest.mark.timeout(30)
async def test_search_with_filters(algolia_connector, test_index):
    """Search with facet filter returns only matching records."""
    records = [
        {"objectID": f"cat-{i}", "name": f"Product {i}", "category": "electronics" if i < 3 else "books"}
        for i in range(6)
    ]
    await algolia_connector.batch_index(records=records, index_name=test_index, wait=True)

    settings_resp = await algolia_connector._run_sync(
        algolia_connector._client.set_settings,
        index_name=test_index,
        index_settings={"attributesForFaceting": ["category"]},
    )
    await algolia_connector.wait_for_task(test_index, getattr(settings_resp, "task_id", None))

    hits = await algolia_connector.search(
        query="Product", index_name=test_index, filters="category:electronics"
    )
    assert hits["nb_hits"] == 3
    for hit in hits["hits"]:
        assert hit["category"] == "electronics"
