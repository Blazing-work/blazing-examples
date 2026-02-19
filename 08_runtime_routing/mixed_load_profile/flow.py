"""
Mixed Load Profile

Demonstrates running a CPU-bound BLOCKING step and an I/O-bound NON-BLOCKING step
concurrently in the same workflow.  asyncio.gather launches both simultaneously so
neither blocks the other, illustrating optimal worker-type selection.

Patterns shown:
  1. BLOCKING step for CPU-bound summation (dedicated thread, doesn't block event loop)
  2. Default NON-BLOCKING step for async I/O (simulated with asyncio.sleep)
  3. asyncio.gather to run both step types concurrently and collect results
"""
import asyncio
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(step_type='BLOCKING')
    async def cpu_work(x: int, services=None):
        total = 0
        for i in range(x):
            total += i
        return total

    @app.step
    async def io_work(x: int, services=None):
        await asyncio.sleep(0.1)
        return x * 2

    @app.workflow
    async def mixed_profile(x: int, services=None):
        cpu, io = await asyncio.gather(
            cpu_work(x, services=services),
            io_work(x, services=services),
        )
        return {'cpu': cpu, 'io': io}

    await app.publish()
    result = await app.mixed_profile(x=1000).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
