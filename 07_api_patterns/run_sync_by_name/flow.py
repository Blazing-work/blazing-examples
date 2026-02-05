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
