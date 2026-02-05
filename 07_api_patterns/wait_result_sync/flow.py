from blazing import Blazing


def main():
    app = Blazing()

    @app.step
    async def increment(x: int, services=None):
        return x + 1

    @app.workflow
    async def inc_twice(value: int, services=None):
        value = await increment(value, services=services)
        value = await increment(value, services=services)
        return value

    app.publish_sync()
    result = app.inc_twice(value=10).wait_result_sync()
    print({'result': result})


if __name__ == '__main__':
    main()
