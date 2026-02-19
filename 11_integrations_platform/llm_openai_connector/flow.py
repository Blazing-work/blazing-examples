"""
OpenAI LLM Connector Example for Blazing

OpenAIConnector wraps the OpenAI chat completions API as a Blazing connector.
Services use it for chat, streaming, tool calling, and multi-turn conversations.

Connector lifecycle:
  connector = OpenAIConnector(api_key="...", model="gpt-4o")
  await connector.connect()
  response = await connector.chat(messages)
  await connector.disconnect()

Or use as an async context manager:
  async with OpenAIConnector(...) as connector:
      ...

Requires: pip install openai
          OPENAI_API_KEY environment variable
"""

import os
from typing import Any, Dict, List

from blazing import Blazing, BaseService
from blazing.local.llm import OpenAIConnector, ChatMessage, ChatResponse
from blazing_service.connectors.secrets import SecretsConnector

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Pattern 1: Simple Chat Service ────────────────────────────────────────────

@app.service
class ChatService(BaseService):
    """Service that wraps OpenAI for single-turn and multi-turn chat."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.llm = (connector_instances or {}).get("openai")
        self.secrets = (connector_instances or {}).get("secrets") or SecretsConnector()

    async def chat(self, user_message: str, system_prompt: str = None) -> str:
        """
        Single-turn chat completion.

        Args:
            user_message: The user's message.
            system_prompt: Optional system instructions.
        Returns:
            Model response text.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        response: ChatResponse = await self.llm.chat(messages)
        return response.content

    async def multi_turn(self, conversation: List[Dict[str, str]]) -> str:
        """
        Continue a multi-turn conversation.

        Args:
            conversation: List of {"role": "user"/"assistant", "content": "..."} dicts.
        Returns:
            Next assistant message.
        """
        response: ChatResponse = await self.llm.chat(conversation)
        return response.content

    async def with_temperature(self, prompt: str, temperature: float = 0.0) -> str:
        """Chat with explicit temperature control."""
        messages = [{"role": "user", "content": prompt}]
        response = await self.llm.chat(messages, temperature=temperature)
        return response.content


# ── Pattern 2: Streaming Service ──────────────────────────────────────────────

@app.service
class StreamingChatService(BaseService):
    """Service that streams token-by-token responses."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.llm = (connector_instances or {}).get("openai")

    async def stream_chat(self, prompt: str) -> str:
        """
        Stream a chat response and return the full text.

        In production: forward chunks to a WebSocket or SSE endpoint.
        """
        full_text = ""
        messages = [{"role": "user", "content": prompt}]

        async for chunk in self.llm.stream(messages):
            full_text += chunk.content
            # In production: yield chunk.content to client

        return full_text


# ── Pattern 3: Tool-Calling Service ───────────────────────────────────────────

@app.service
class ToolCallingService(BaseService):
    """Service that uses function calling / tool use."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.llm = (connector_instances or {}).get("openai")

    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"},
                    },
                    "required": ["city"],
                },
            },
        }
    ]

    async def ask_with_tools(self, question: str) -> dict:
        """
        Ask the model a question with tool-calling enabled.

        Returns either a text answer or the tool call the model requested.
        """
        messages = [{"role": "user", "content": question}]
        response = await self.llm.chat(messages, tools=self.TOOLS)

        if response.tool_calls:
            return {
                "type": "tool_call",
                "tool": response.tool_calls[0]["function"]["name"],
                "args": response.tool_calls[0]["function"]["arguments"],
            }
        return {"type": "text", "content": response.content}


# ── Workflows ─────────────────────────────────────────────────────────────────

@app.workflow
async def summarize_article(article: str, services=None) -> str:
    """Summarize an article using the chat service."""
    svc = services.get("ChatService")
    return await svc.chat(
        f"Summarize this article in 2 sentences:\n\n{article}",
        system_prompt="You are a concise technical writer.",
    )


@app.workflow
async def analyze_sentiment(texts: list, services=None) -> list:
    """Analyze sentiment for a list of texts."""
    svc = services.get("ChatService")
    results = []
    for text in texts:
        label = await svc.with_temperature(
            f"Classify sentiment as POSITIVE, NEGATIVE, or NEUTRAL: {text}",
            temperature=0.0,
        )
        results.append({"text": text, "sentiment": label.strip()})
    return results


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY to run this example.")
        return

    print("=== OpenAI LLM Connector Demo ===")
    print()

    async with OpenAIConnector(api_key=api_key, model="gpt-4o-mini") as connector:
        # Single-turn
        svc = ChatService(connector_instances={"openai": connector})
        answer = await svc.chat(
            "What is 2 + 2?",
            system_prompt="Answer concisely in one sentence.",
        )
        print(f"Chat: {answer}")

        # Multi-turn
        conversation = [
            {"role": "user",      "content": "My name is Alex."},
            {"role": "assistant", "content": "Hello Alex, nice to meet you!"},
            {"role": "user",      "content": "What is my name?"},
        ]
        name = await svc.multi_turn(conversation)
        print(f"Multi-turn: {name}")
        print()

    print("Response fields: content, role, model, finish_reason, usage")
    print("usage: {prompt_tokens, completion_tokens, total_tokens}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
