"""
Run Sync by Name

Demonstrates the synchronous publish-and-run API using publish_sync() and run_sync().
No async/await is required at the call site — Blazing manages the event loop internally,
making it easy to use from synchronous Python scripts.

Patterns shown:
  1. app.publish_sync() — synchronous publish from a regular def function
  2. app.run_sync('workflow_name', **kwargs) — execute workflow by name and get result
  3. Entirely synchronous def main() without asyncio.run()
"""
from blazing import Blazing


def main():
    app = Blazing()

    @app.step
    async def square(x: int, services=None):
        return x * x

    @app.workflow
    async def compute(value: int, services=None):
        return await square(value, services=services)

    app.publish_sync()
    result = app.run_sync('compute', value=9)
    print({'result': result})


if __name__ == '__main__':
    main()
