import asyncio
            import uvicorn
            from fastapi import FastAPI
            from fastapi.responses import StreamingResponse
            from blazing import Blazing
            from blazing.web import create_asgi_app


            async def main():
                app = Blazing()

                @app.endpoint(path='/double', method='POST')
                @app.workflow
                async def double(value: int, services=None):
                    return {'value': value * 2}

                await app.publish()
                blazing_asgi = await create_asgi_app(app)

                api = FastAPI()
                api.mount('/blazing', blazing_asgi)

                async def event_stream():
                    for i in range(5):
                        yield f"data: tick {i}

"
                        await asyncio.sleep(0.5)

                @api.get('/stream')
                async def stream():
                    return StreamingResponse(event_stream(), media_type='text/event-stream')

                uvicorn.run(api, host='0.0.0.0', port=8080)


            if __name__ == '__main__':
                import asyncio

                asyncio.run(main())
