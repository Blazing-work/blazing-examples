"""
# Hello World

Deploy your first serverless function in under 5 minutes.

## Metadata
- **Product**: Blazing Core
- **Difficulty**: Beginner
- **Time**: 5 min
- **Tags**: quickstart, python

## Description

This is the simplest possible Blazing Core application. It demonstrates how to:
- Create a basic Blazing app
- Deploy a simple function
- Return a response

## What you'll learn

- How to structure a Blazing Core application
- Basic deployment workflow
- Function routing and responses
"""

from blazing import Blazing

app = Blazing()


@app.function()
def hello():
    """A simple hello world function."""
    return {"message": "Hello, World!"}


@app.function()
def hello_name(name: str):
    """A personalized greeting function."""
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    # Test locally
    print(hello())
    print(hello_name("Blazing"))
