"""
LangBlaze LLM Service Example

LangBlaze bridges Blazing's trusted-service execution model with LangChain.
LLM calls from sandboxed Pyodide steps are routed through a trusted LLMService
that holds the real API key — the sandbox never sees the key.

Architecture:
  ┌───────────────────────────────────────────────────────────────┐
  │  TRUSTED WORKERS              │  SANDBOXED (Pyodide WASM)     │
  │  ──────────────────           │  ──────────────────────────   │
  │  LLMService                   │  @app.step(sandboxed=True)    │
  │    connector → OpenAI API     │    LLM(services, model=...)   │
  │    returns plain dict         │    → BaseChatModel adapter    │
  │                               │    LangChain LCEL chains      │
  └───────────────────────────────────────────────────────────────┘

Key components:
  LLMService  — trusted service; proxies chat requests to connectors
  LLM         — LangChain BaseChatModel adapter; used inside sandbox steps
  OpenAIConnector / AnthropicConnector — hold real API keys on trusted workers

Patterns shown:
  1. Basic LLM call from sandbox via LLM adapter
  2. LangChain LCEL chain in sandboxed step
  3. Multi-turn conversation with history
  4. Tool calling from sandbox

Requires: pip install langblaze langchain-core langchain-openai
          docker-compose up -d
          OPENAI_API_KEY environment variable
"""

import os

from blazing import Blazing
from blazing.local.llm import OpenAIConnector
from langblaze import LLM, LLMService


app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)

# Register LLMService with the OpenAI connector
# LLMService runs on trusted workers; the sandbox step calls it via services=
llm_service = LLMService(connectors={
    "openai": OpenAIConnector(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model="gpt-4o-mini",
    )
})
app.register_service(llm_service, name="LLMService")


# ── Pattern 1: Basic LLM call from sandboxed step ────────────────────────────

@app.step(sandboxed=True)
async def classify_intent(text: str, services=None) -> dict:
    """
    Classify user intent using an LLM inside the Pyodide sandbox.

    LLM(services) creates a LangChain BaseChatModel that routes through
    LLMService on the trusted worker — the API key never enters the sandbox.
    """
    from langchain_core.messages import HumanMessage, SystemMessage

    model = LLM(services, model="gpt-4o-mini")

    messages = [
        SystemMessage(content="Classify intent as: question, command, or statement. Reply with one word."),
        HumanMessage(content=text),
    ]
    response = await model.ainvoke(messages)
    return {"text": text, "intent": response.content.strip().lower()}


# ── Pattern 2: LangChain LCEL chain in sandboxed step ────────────────────────

@app.step(sandboxed=True)
async def run_lcel_chain(topic: str, services=None) -> str:
    """
    Run a LangChain LCEL chain entirely inside the Pyodide sandbox.

    LCEL (LangChain Expression Language) chains work with the LLM adapter
    the same way they work with any LangChain chat model.
    """
    from langchain_core.messages import HumanMessage
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    model = LLM(services, model="gpt-4o-mini")

    # Build a prompt template → model → string output chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise technical writer. Answer in exactly 2 sentences."),
        ("user", "Explain: {topic}"),
    ])
    chain = prompt | model | StrOutputParser()

    return await chain.ainvoke({"topic": topic})


# ── Pattern 3: Multi-turn conversation ────────────────────────────────────────

@app.step(sandboxed=True)
async def multi_turn_chat(history: list, new_message: str, services=None) -> dict:
    """
    Continue a multi-turn conversation with message history.

    history: List of {"role": "user"|"assistant", "content": "..."} dicts.
    """
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    model = LLM(services, model="gpt-4o-mini")

    # Reconstruct message history
    messages = [SystemMessage(content="You are a helpful assistant.")]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=new_message))

    response = await model.ainvoke(messages)
    updated_history = history + [
        {"role": "user",      "content": new_message},
        {"role": "assistant", "content": response.content},
    ]
    return {"response": response.content, "history": updated_history}


# ── Pattern 4: Structured output with output parser ──────────────────────────

@app.step(sandboxed=True)
async def extract_entities(text: str, services=None) -> dict:
    """
    Extract named entities using a structured prompt chain.
    """
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_core.output_parsers import JsonOutputParser

    model = LLM(services, model="gpt-4o-mini")

    messages = [
        SystemMessage(content=(
            "Extract entities from text. "
            "Return JSON with keys: people (list), places (list), organizations (list)."
        )),
        HumanMessage(content=text),
    ]
    response = await model.ainvoke(messages)

    try:
        import json
        # Strip markdown code fences if present
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content.strip())
    except Exception:
        return {"raw": response.content, "people": [], "places": [], "organizations": []}


# ── Workflows ─────────────────────────────────────────────────────────────────

@app.workflow
async def analyze_texts(texts: list, services=None) -> list:
    """Classify intent for multiple texts in parallel."""
    results = []
    for text in texts:
        result = await classify_intent(text)
        results.append(result)
    return results


@app.workflow
async def explain_concepts(topics: list, services=None) -> dict:
    """Explain multiple technical concepts via LCEL chain."""
    explanations = {}
    for topic in topics:
        explanations[topic] = await run_lcel_chain(topic)
    return explanations


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY to run this example.")
        return

    print("=== LangBlaze LLM Service Demo ===")
    print()
    print("Architecture:")
    print("  Sandboxed step → LLM(services) → LLMService (trusted) → OpenAI")
    print()

    await app.publish()

    # Intent classification
    results = await app.run(analyze_texts, args=([
        "What is the capital of France?",
        "Delete all files in /tmp",
        "The sky is blue.",
    ],))
    for r in results:
        print(f"  [{r['intent']:10s}] {r['text']}")
    print()

    # LCEL chain
    explanations = await app.run(explain_concepts, args=(["LangChain LCEL", "Pyodide sandbox"],))
    for topic, explanation in explanations.items():
        print(f"--- {topic} ---")
        print(explanation)
        print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
