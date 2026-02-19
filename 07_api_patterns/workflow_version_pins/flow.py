"""
Workflow Version Pins

Demonstrates pinning specific service versions for a workflow using the version_pins
parameter on @app.workflow.  Version pinning ensures the workflow always uses a declared
service version, enabling reproducible deployments regardless of the latest published version.

Patterns shown:
  1. version_pins dict mapping service name to a version string
  2. Passing version_pins= to @app.workflow decorator
  3. Running the pinned workflow and retrieving the result
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step
    async def multiply(x: int, services=None):
        return x * 3

    version_pins = {
        'MathService': '1.0.0',
    }

    @app.workflow(version_pins=version_pins)
    async def pinned_workflow(x: int, services=None):
        return await multiply(x, services=services)

    await app.publish()
    result = await app.pinned_workflow(x=7).wait_result()
    print({'result': result})


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
