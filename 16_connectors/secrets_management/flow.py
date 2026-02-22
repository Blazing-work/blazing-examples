"""
Secrets Management with SecretsConnector

Store and retrieve encrypted secrets through trusted services using LocalSecretsService
and SecretsConnector. Sandboxed steps cannot access secrets directly — only trusted
services can, enforcing the same security model as database connectors.

Patterns shown:
  1. LocalStack + LocalSecretsService — local emulator for dev/test
  2. Secret.from_dict({...}) — create secrets from key-value dict
  3. SecretsConnector — injected into services, provides .get() and .as_env_dict()
  4. DatabaseService(BaseService) — trusted service fetching DATABASE_URL, DB_USER, DB_PASSWORD
  5. APIClientService(BaseService) — trusted service fetching API_KEY, API_SECRET
  6. secrets.get("KEY") — async secret lookup inside service methods
  7. secrets.as_env_dict() — get all secrets as env var dict

Requires: pip install blazing
          docker-compose up -d (or LocalStack for local dev)
"""

import asyncio
import tempfile
from pathlib import Path

from blazing import LocalStack
from blazing.local import LocalSecretsService, SecretsConnector, Secret
from blazing.base import BaseService


# ── DatabaseService — trusted service, uses secrets to supply DB credentials ──

class DatabaseService(BaseService):
    """
    Trusted service that retrieves database credentials from a SecretsConnector.
    Sandboxed steps call service methods instead of accessing secrets directly.
    """
    def __init__(self, connector_instances=None):
        self.connector_instances = connector_instances
        self.secrets = connector_instances.get('secrets') if connector_instances else None

    async def get_connection_string(self) -> dict:
        """Return DATABASE_URL from secrets."""
        db_url = await self.secrets.get("DATABASE_URL")
        return {"url": db_url, "connected": db_url is not None}

    async def get_credentials(self) -> dict:
        """Return DB_USER (with default) and whether DB_PASSWORD is set."""
        username = await self.secrets.get("DB_USER", "default_user")
        password = await self.secrets.get("DB_PASSWORD")
        return {
            "username": username,
            "password_set": password is not None,
        }


# ── APIClientService — trusted service, uses secrets for API auth ──────────────

class APIClientService(BaseService):
    """
    Trusted service that retrieves API credentials from a SecretsConnector.
    """
    def __init__(self, connector_instances=None):
        self.connector_instances = connector_instances
        self.secrets = connector_instances.get('api_credentials') if connector_instances else None

    async def make_authenticated_request(self, endpoint: str) -> dict:
        """Simulate API call — returns whether credentials were present."""
        api_key = await self.secrets.get("API_KEY")
        api_secret = await self.secrets.get("API_SECRET")
        return {
            "endpoint": endpoint,
            "authenticated": api_key is not None,
            "has_api_key": bool(api_key),
            "has_api_secret": api_secret is not None,
        }

    async def get_env_vars(self) -> dict:
        """Return all secrets as a flat env var dict."""
        env_dict = self.secrets.as_env_dict()
        return {"count": len(env_dict), "keys": list(env_dict.keys())}


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    print("=== Secrets Management with SecretsConnector ===")
    print()

    with tempfile.TemporaryDirectory(prefix="blazing-secrets-") as tmp:
        storage_path = Path(tmp)

        # ── Pattern 1: LocalSecretsService standalone ─────────────────────────
        print("--- Pattern 1: DatabaseService with SecretsConnector ---")
        secrets_svc = LocalSecretsService(storage_path=str(storage_path / "secrets"))
        await secrets_svc.start()

        secret = Secret.from_dict({
            "DATABASE_URL": "postgres://localhost:5432/mydb",
            "DB_USER":      "admin",
            "DB_PASSWORD":  "super-secret",
        })
        await secrets_svc.save_secret("db-credentials", secret)

        connector = await secrets_svc.get_connector("db-credentials")
        db_service = DatabaseService({'secrets': connector})

        conn = await db_service.get_connection_string()
        creds = await db_service.get_credentials()
        print(f"  Connection URL present: {conn['connected']}")
        print(f"  DB user: {creds['username']}, password set: {creds['password_set']}")
        await connector.disconnect()

        # ── Pattern 2: APIClientService with secrets ──────────────────────────
        print()
        print("--- Pattern 2: APIClientService with SecretsConnector ---")
        api_secret = Secret.from_dict({
            "API_KEY":    "pk_live_abc123",
            "API_SECRET": "sk_live_xyz789",
            "API_VERSION": "v2",
        })
        await secrets_svc.save_secret("api-creds", api_secret)

        api_connector = await secrets_svc.get_connector("api-creds")
        api_service = APIClientService({'api_credentials': api_connector})

        auth_result = await api_service.make_authenticated_request("/users")
        env_result  = await api_service.get_env_vars()
        print(f"  Authenticated: {auth_result['authenticated']}")
        print(f"  Secret env vars: {env_result['count']} ({env_result['keys']})")
        await api_connector.disconnect()

        # ── Pattern 3: LocalStack wraps both services ──────────────────────────
        print()
        print("--- Pattern 3: LocalStack with secrets service ---")
        stack = LocalStack(storage_path=str(storage_path / "stack"))
        await stack.start(start_registry_server=False)

        stack_secret = Secret.from_dict({"STRIPE_KEY": "sk_live_xxx", "WEBHOOK_SECRET": "whsec_xxx"})
        await stack.secrets_service.save_secret("stripe", stack_secret)

        stripe_connector = await stack.secrets_service.get_connector("stripe")
        stripe_key = await stripe_connector.get("STRIPE_KEY")
        print(f"  Stripe key starts with: {stripe_key[:7]}...")
        await stripe_connector.disconnect()

        stats = stack.get_stats()
        print(f"  Total secrets: {stats['secrets']['total_secrets']}")
        await stack.stop()
        await secrets_svc.stop()

    print()
    print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
