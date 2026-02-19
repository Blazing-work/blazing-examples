"""
Google Sheets connector tests — real Sheets API operations.

Validates read, write, append, and batch update against a live spreadsheet.
The test spreadsheet must have "Sheet1" and "E2ETest" tabs.

Run:
    GOOGLE_SHEETS_CREDENTIALS='{"type":"service_account",...}' \
    GOOGLE_SHEETS_TEST_SPREADSHEET_ID=1BxiMVs0... \
    pytest 15_connector_tests/google_sheets/ -v
"""

import os
import time
import pytest

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(
        not os.getenv("GOOGLE_SHEETS_CREDENTIALS"),
        reason="GOOGLE_SHEETS_CREDENTIALS not set",
    ),
]

requires_sheet_id = pytest.mark.skipif(
    not os.getenv("GOOGLE_SHEETS_TEST_SPREADSHEET_ID"),
    reason="GOOGLE_SHEETS_TEST_SPREADSHEET_ID not set",
)


@requires_sheet_id
@pytest.mark.timeout(30)
async def test_read_values(google_sheets_connector):
    """Read rows from Sheet1 — spreadsheet must have at least one row."""
    rows = await google_sheets_connector.read_rows(
        spreadsheet_id=os.getenv("GOOGLE_SHEETS_TEST_SPREADSHEET_ID"),
        worksheet="Sheet1",
        range="A1:B2",
    )
    assert isinstance(rows, list)
    assert len(rows) > 0


@requires_sheet_id
@pytest.mark.timeout(30)
async def test_write_and_read_back(google_sheets_connector):
    """Write 2x2 block and read it back byte-for-byte."""
    sid = os.getenv("GOOGLE_SHEETS_TEST_SPREADSHEET_ID")
    data = [["name", "value"], ["e2e_test", "42"]]

    write = await google_sheets_connector.write_cells(
        spreadsheet_id=sid, worksheet="E2ETest", range="A1:B2", values=data
    )
    assert write["updated_cells"] == 4

    read = await google_sheets_connector.read_rows(
        spreadsheet_id=sid, worksheet="E2ETest", range="A1:B2"
    )
    assert read == data


@requires_sheet_id
@pytest.mark.timeout(30)
async def test_append_row(google_sheets_connector):
    """Append a timestamped row and verify it appears in the sheet."""
    sid = os.getenv("GOOGLE_SHEETS_TEST_SPREADSHEET_ID")
    ts = str(time.time())
    result = await google_sheets_connector.append_rows(
        spreadsheet_id=sid, rows=[["appended", ts]], worksheet="E2ETest"
    )
    assert result["appended_rows"] == 1

    all_rows = await google_sheets_connector.read_rows(
        spreadsheet_id=sid, worksheet="E2ETest", range="A:B"
    )
    assert any(len(r) >= 2 and r[0] == "appended" and r[1] == ts for r in all_rows)


@requires_sheet_id
@pytest.mark.timeout(30)
async def test_batch_update(google_sheets_connector):
    """Batch update two cells and verify each independently."""
    sid = os.getenv("GOOGLE_SHEETS_TEST_SPREADSHEET_ID")
    result = await google_sheets_connector.batch_update(
        spreadsheet_id=sid,
        updates=[{"range": "C1", "values": [["batch1"]]}, {"range": "D1", "values": [["batch2"]]}],
        worksheet="E2ETest",
    )
    assert result["updated_ranges"] == 2

    assert await google_sheets_connector.read_rows(spreadsheet_id=sid, worksheet="E2ETest", range="C1") == [["batch1"]]
    assert await google_sheets_connector.read_rows(spreadsheet_id=sid, worksheet="E2ETest", range="D1") == [["batch2"]]
