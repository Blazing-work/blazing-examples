"""
Direct Function Call Pattern

@app.step and @app.workflow decorated functions are callable as plain Python
functions — no backend, no publish(), no infrastructure required.

This is the recommended way to:
- Unit test individual steps in isolation
- Develop and iterate on logic without spinning up Docker
- Run examples in CI without credentials

How it works:
  When called outside a running workflow, `enqueue_var` stays False, so the
  decorator executes the function in-process and returns the result directly.
  When the executor runs the same code inside a distributed workflow, it sets
  `enqueue_var=True` and the decorator enqueues to the backend instead.
"""

from blazing import Blazing


async def main():
    # Dummy credentials — no real backend needed for direct calls
    app = Blazing(api_url="http://localhost:8000", api_token="test-token")

    @app.step
    async def normalize(value: float, services=None) -> float:
        """Scale a value to the 0–1 range (input assumed 0–100)."""
        return value / 100.0

    @app.step
    async def format_result(value: float, services=None) -> str:
        """Format a float as a percentage string."""
        return f"{value:.1%}"

    @app.workflow
    async def score_to_label(raw_score: float, services=None) -> str:
        """Convert a raw 0–100 score to a formatted percentage label."""
        normalized = await normalize(raw_score, services=services)
        return await format_result(normalized, services=services)

    # Call steps directly — executes in-process, no publish() needed
    assert await normalize(75.0) == 0.75
    assert await format_result(0.75) == "75.0%"

    # Call workflow directly — all steps run locally too
    result = await score_to_label(raw_score=92.5)
    assert result == "92.5%"

    print({"result": result})


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
