"""
Streaming Progress Bar

Demonstrates streaming real-time progress updates from a Blazing workflow endpoint using
the progress_bar helper and send_data.  The endpoint streams partial sum results to the
client as each item is processed, then returns the final total.

Patterns shown:
  1. @app.endpoint(path='/sum', response_mode='stream') for a streaming HTTP endpoint
  2. progress_bar(values, message_template=...) to iterate with progress messages
  3. send_data({'partial_sum': total}, label='partial') to push intermediate results
"""
import asyncio
import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app
from blazing.endpoints.streaming import progress_bar, send_data


async def main():
    app = Blazing()

    @app.endpoint(path='/sum', response_mode='stream')
    @app.workflow
    async def sum_numbers(values: list, services=None):
        total = 0
        async for value in progress_bar(values, message_template='Summing {current}/{total}'):
            await asyncio.sleep(0.1)
            total += value
            await send_data({'partial_sum': total}, label='partial')
        return {'sum': total}

    await app.publish()
    fastapi_app = await create_asgi_app(app)
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
