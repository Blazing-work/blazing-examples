# LangBlaze LLM Service

Run LangChain LCEL chains inside the Pyodide sandbox, routing LLM calls through a trusted service.

## Architecture

```
Sandboxed step (Pyodide WASM)          Trusted worker
──────────────────────────────         ───────────────────────────
LangChain chain                   →    LLMService.achat(messages)
  prompt | LLM(services) | parser           ↓
                                       OpenAIConnector → OpenAI API
```

The sandbox never holds an API key. `LLM(services)` is a `BaseChatModel` adapter that serializes LangChain messages to plain dicts, calls `LLMService` on the trusted worker, and returns the response as a LangChain `AIMessage`.

## API

```python
from langblaze import LLM, LLMService
from blazing.local.llm import OpenAIConnector

# Register at app level (trusted worker side)
llm_service = LLMService(connectors={
    "openai": OpenAIConnector(api_key="...", model="gpt-4o-mini"),
})
app.register_service(llm_service, name="LLMService")

# Inside sandboxed step (Pyodide sandbox)
@app.step(sandboxed=True)
async def my_agent(text: str, services=None) -> str:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    model = LLM(services, model="gpt-4o-mini")

    # LangChain LCEL chain — works exactly like any BaseChatModel
    chain = ChatPromptTemplate.from_messages([
        ("system", "Answer in one sentence."),
        ("user",   "{question}"),
    ]) | model | StrOutputParser()

    return await chain.ainvoke({"question": text})
```

## Supported Connectors

| Connector | Import |
|-----------|--------|
| `OpenAIConnector` | `from blazing.local.llm import OpenAIConnector` |
| `AnthropicConnector` | `from blazing.local.llm import AnthropicConnector` |

## Patterns

| Pattern | Description |
|---------|-------------|
| Basic call | `await model.ainvoke(messages)` |
| LCEL chain | `prompt \| model \| StrOutputParser()` |
| Multi-turn | Pass `AIMessage` + `HumanMessage` history |
| Tool calling | `model.bind_tools(tools)` |
| Structured output | Use `JsonOutputParser` or `model.with_structured_output(schema)` |

## Requirements

```bash
pip install langblaze langchain-core langchain-openai
docker-compose up -d
export OPENAI_API_KEY=sk-...
python flow.py
```
