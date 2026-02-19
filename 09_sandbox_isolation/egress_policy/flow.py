"""
Egress Policy Example for Blazing

Demonstrates how to declare outbound network access rules on a service.
When Blazing runs a service step in a sandboxed worker, it installs a
sys.audit hook that enforces the declared egress allowlist.

Egress declaration syntax (on @app.service):

    egress=["api.openai.com"]           # exact hostname
    egress=["*.anthropic.com"]          # wildcard — any subdomain
    egress=["10.0.0.0/8"]              # CIDR block (private network)
    egress=["api.a.com", "api.b.com"]  # multiple destinations
    egress=[]                           # deny all outbound (maximum isolation)
    (no egress=)                        # no restriction (legacy / open mode)

Enforcement modes (BLAZING_EGRESS_MODE environment variable):
    DENY_BY_DEFAULT  — block undeclared destinations  [production default]
    AUDIT_ONLY       — log violations, never block    [dry-run rollout]
    ALLOW_ALL        — no enforcement                  [local development]

SYSTEM DEPENDENCY: Egress enforcement requires running with Docker
infrastructure. Run `docker-compose up -d` before using app.publish().
"""

import os

from blazing import Blazing, BaseService
from blazing_service.connectors.secrets import SecretsConnector

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Pattern 1: Single external API ──────────────────────────────────────────

@app.service(egress=["api.openai.com"])
class SummarizationService(BaseService):
    """Service that calls the OpenAI API only.

    Any connection attempt to a host other than api.openai.com
    raises ConnectionRefusedError with "egress" in the message.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.secrets = (connector_instances or {}).get("secrets") or SecretsConnector()

    async def summarize(self, text: str) -> str:
        import httpx

        api_key = await self.secrets.get("OPENAI_API_KEY")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": f"Summarize: {text[:500]}"}],
                    "max_tokens": 150,
                },
            )
        return resp.json()["choices"][0]["message"]["content"]


# ── Pattern 2: Wildcard subdomain ────────────────────────────────────────────

@app.service(egress=["*.anthropic.com"])
class ClaudeService(BaseService):
    """Service that may connect to any *.anthropic.com subdomain.

    Matches:  api.anthropic.com, claude.anthropic.com, …
    Blocks:   api.openai.com, evil.com, …
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.secrets = (connector_instances or {}).get("secrets") or SecretsConnector()

    async def ask(self, prompt: str) -> str:
        import httpx

        api_key = await self.secrets.get("ANTHROPIC_API_KEY")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 150,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        return resp.json()["content"][0]["text"]


# ── Pattern 3: Multiple allowed destinations ─────────────────────────────────

@app.service(egress=["api.openai.com", "api.stripe.com"])
class PaymentAIService(BaseService):
    """Service that orchestrates OpenAI analysis and Stripe payments.

    Declares exactly the two external APIs it needs — nothing more.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)


# ── Pattern 4: Full isolation (deny all outbound) ────────────────────────────

@app.service(egress=[])
class IsolatedComputeService(BaseService):
    """Pure compute service — zero outbound network access.

    Use for CPU-only tasks, data transformations, or cryptographic
    operations that should have no network access whatsoever.
    """

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)

    async def compute_stats(self, data: list) -> dict:
        """Pure computation — no network needed."""
        if not data:
            return {"count": 0, "total": 0, "mean": 0}
        return {
            "count": len(data),
            "total": sum(data),
            "mean": sum(data) / len(data),
            "min": min(data),
            "max": max(data),
        }


@app.workflow
async def analyze_and_pay(text: str, amount_cents: int, services=None) -> dict:
    """Example workflow: summarize text then process payment."""
    # In a real workflow, steps would be @app.step decorated functions
    return {
        "text_length": len(text),
        "amount_cents": amount_cents,
        "status": "workflow_defined",
    }


if __name__ == "__main__":
    import asyncio

    async def show_egress_patterns():
        print("Egress Policy Patterns:")
        print()
        print("  @app.service(egress=['api.openai.com'])")
        print("    → exact hostname match")
        print()
        print("  @app.service(egress=['*.anthropic.com'])")
        print("    → wildcard subdomain (any *.anthropic.com host)")
        print()
        print("  @app.service(egress=['api.a.com', 'api.b.com'])")
        print("    → multiple destinations")
        print()
        print("  @app.service(egress=[])")
        print("    → deny ALL outbound (maximum isolation)")
        print()
        print("  @app.service()")
        print("    → no restriction (development / legacy mode)")
        print()
        print("Enforcement modes via BLAZING_EGRESS_MODE:")
        print("  DENY_BY_DEFAULT  → block undeclared  [production default]")
        print("  AUDIT_ONLY       → log, never block  [dry-run]")
        print("  ALLOW_ALL        → no enforcement    [local dev]")
        print()

        # Demonstrate isolated service locally (no Docker needed for this)
        svc = IsolatedComputeService()
        result = await svc.compute_stats([1, 2, 3, 4, 5])
        print(f"IsolatedComputeService.compute_stats([1,2,3,4,5]) = {result}")

    asyncio.run(show_egress_patterns())
