"""
Local Dict Connector

Demonstrates using LocalDictService as an in-process shared key-value store to maintain
workflow state across iterations.  A dict is created, a state value is stored and
incremented in a loop, then the final state is retrieved and printed.

Patterns shown:
  1. LocalDictService(cleanup_interval=...) for an in-process dict service
  2. service.create_dict('name') to create a named dict instance
  3. state_dict.put(key, value) and state_dict.get(key) for read/write access
"""
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
