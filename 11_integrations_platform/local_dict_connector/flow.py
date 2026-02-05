from blazing.local import LocalDictService


async def main():
    service = LocalDictService(cleanup_interval=60.0)
    await service.start()

    state = {'value': 0, 'history': []}
    state_dict = await service.create_dict('workflow-state')
    await state_dict.put('state', state)

    while state['value'] < 3:
        state = await state_dict.get('state')
        state['value'] += 1
        state['history'].append(state['value'])
        await state_dict.put('state', state)

    final_state = await state_dict.get('state')
    print(final_state)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
