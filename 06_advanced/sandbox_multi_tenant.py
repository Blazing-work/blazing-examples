"""
# Sandbox: Multi-Tenant Data Processing

Safely run different tenants' code in isolated sandboxes.

## Metadata
- **Product**: Blazing Flow Sandbox
- **Difficulty**: Expert
- **Time**: 35 min
- **Tags**: sandbox, multi-tenant, isolation, security

## Description

Safely run different tenants' code in isolated sandboxes.

## What you'll learn

- Multi-tenant code execution patterns
- Tenant data isolation strategies
- Running different tenant code safely
"""

from blazing import Blazing
from blazing.base import BaseService

async def main():
    app = Blazing()  # Uses Blazing SaaS by default
    # YOUR CODE (trusted - manages tenant data)
    @app.service
    class TenantDataService(BaseService):
        def __init__(self, connectors):
            self._db = connectors.get('postgres')
        async def get_tenant_data(self, tenant_id: str) -> list:
            """Fetch data for specific tenant."""
            query = text("""
                SELECT * FROM data
                WHERE tenant_id = :tenant_id
                AND deleted_at IS NULL
            """)
            result = await self._db.execute(query, {"tenant_id": tenant_id})
            return [dict(row) for row in result]
        async def save_tenant_results(self, tenant_id: str, results: list):
            """Save processed results for tenant."""
            for item in results:
                query = text("""
                    INSERT INTO results (tenant_id, data, created_at)
                    VALUES (:tenant_id, :data, NOW())
                """)
                await self._db.execute(query, {
                    "tenant_id": tenant_id,
                    "data": json.dumps(item)
                })
            await self._db.commit()
    # TENANT A's CODE (untrusted - runs in WASM)
    @app.step
    async def tenant_a_transform(tenant_id: str, services=None):
        """Tenant A's custom transformation logic."""
        data = await services['TenantDataService'].get_tenant_data(tenant_id)
        # Tenant A's processing logic
        results = [
            {"value": item["value"] * 2, "label": "doubled"}
            for item in data
        ]
        await services['TenantDataService'].save_tenant_results(tenant_id, results)
        return {"processed": len(results), "tenant": tenant_id}
    # TENANT B's CODE (untrusted - runs in WASM)
    @app.step
    async def tenant_b_transform(tenant_id: str, services=None):
        """Tenant B's custom transformation logic (different from Tenant A)."""
        data = await services['TenantDataService'].get_tenant_data(tenant_id)
        # Tenant B's processing logic (different algorithm)
        results = [
            {"value": item["value"] ** 2, "label": "squared"}
            for item in data
        ]
        await services['TenantDataService'].save_tenant_results(tenant_id, results)
        return {"processed": len(results), "tenant": tenant_id}
    # YOUR CODE (trusted - routes to correct tenant code)
    @app.workflow
    async def process_tenant_data(tenant_id: str, services=None):
        """Route to correct tenant's processing logic."""
        if tenant_id == "tenant_a":
            return await tenant_a_transform(tenant_id, services=services)
        elif tenant_id == "tenant_b":
            return await tenant_b_transform(tenant_id, services=services)
        else:
            raise ValueError(f"Unknown tenant: {tenant_id}")
    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
