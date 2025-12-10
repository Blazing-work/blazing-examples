"""
# Data Processing Step

Filter and transform data in a single step.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: step, data, filtering

## Description

Filter and transform data in a single step.

## What you'll learn

- How to work with lists in steps
- How to use list comprehensions for data filtering
- Basic data transformation patterns
"""



from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def filter_positive(numbers: list, services=None):
        """Filter out negative numbers."""
        return [n for n in numbers if n > 0]

    await app.publish()
    result = await app.filter_positive([1, -2, 3, -4, 5])
    print(result)  # [1, 3, 5]


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
