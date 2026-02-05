from blazing import SyncBlazing


def main():
    app = SyncBlazing()

    @app.step
    async def add(x: int, y: int, services=None):
        return x + y

    @app.workflow
    async def add_two_numbers(x: int, y: int, services=None):
        return await add(x, y, services=services)

    app.publish()
    result = app.add_two_numbers(x=5, y=7)
    print({'result': result})


if __name__ == '__main__':
    main()
