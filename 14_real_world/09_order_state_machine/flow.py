"""
Order Processing State Machine

A realistic state machine where each transition is a sandboxed step that
calls a trusted service to check payment and inventory before approving
or rejecting an order.

State transitions:
    PENDING → PAYMENT_CHECK → INVENTORY_CHECK → APPROVED → COMPLETED
                            ↘                ↘
                             REJECTED ──────── FAILED

Architecture:
    @app.service  OrderService    — simulates DB lookups (trusted worker)
    @app.step(sandboxed=True)     — transition logic (Pyodide sandbox)
    @app.workflow                 — orchestrates the state machine loop
"""

from blazing import Blazing, BaseService


async def main():
    app = Blazing()

    # -------------------------------------------------------------------------
    # Service: simulates database lookups (runs on trusted worker)
    # -------------------------------------------------------------------------

    @app.service
    class OrderService(BaseService):
        connector_instances = None

        def __init__(self, connector_instances=None):
            self._payments = {
                "ORD-001": {"valid": True, "amount": 99.99},
                "ORD-002": {"valid": True, "amount": 249.99},
                "ORD-003": {"valid": False, "amount": 0.0},
            }
            self._inventory = {
                "ORD-001": {"in_stock": True, "available": 10},
                "ORD-002": {"in_stock": False, "available": 0},
                "ORD-003": {"in_stock": True, "available": 500},
            }

        async def check_payment(self, order_id: str) -> dict:
            p = self._payments.get(order_id, {"valid": False})
            return {"valid": p["valid"], "reason": "ok" if p["valid"] else "declined"}

        async def check_inventory(self, order_id: str) -> dict:
            inv = self._inventory.get(order_id, {"in_stock": False, "available": 0})
            return {"in_stock": inv["in_stock"], "available": inv["available"]}

        async def finalize(self, order_id: str, status: str) -> dict:
            return {"order_id": order_id, "status": status}

    # -------------------------------------------------------------------------
    # Step: one state-machine transition (runs in sandbox, calls service)
    # -------------------------------------------------------------------------

    @app.step(sandboxed=True)
    async def transition(state: dict, services=None) -> dict:
        order_id = state["order_id"]
        current = state["current_state"]
        history = state.get("history", [])
        terminal = {"COMPLETED", "FAILED"}

        if current in terminal:
            return state

        next_state = current

        if current == "PENDING":
            next_state = "PAYMENT_CHECK"

        elif current == "PAYMENT_CHECK":
            result = await services["OrderService"].check_payment(order_id)
            next_state = "INVENTORY_CHECK" if result["valid"] else "REJECTED"

        elif current == "INVENTORY_CHECK":
            result = await services["OrderService"].check_inventory(order_id)
            next_state = "APPROVED" if result["in_stock"] else "REJECTED"

        elif current == "APPROVED":
            await services["OrderService"].finalize(order_id, "COMPLETED")
            next_state = "COMPLETED"

        elif current == "REJECTED":
            await services["OrderService"].finalize(order_id, "FAILED")
            next_state = "FAILED"

        if next_state != current:
            history.append({"from": current, "to": next_state})

        return {
            "order_id": order_id,
            "current_state": next_state,
            "history": history,
            "done": next_state in terminal,
        }

    # -------------------------------------------------------------------------
    # Workflow: drive the state machine to completion
    # -------------------------------------------------------------------------

    @app.workflow
    async def process_order(order_id: str, services=None) -> dict:
        state = {
            "order_id": order_id,
            "current_state": "PENDING",
            "history": [],
            "done": False,
        }
        while not state["done"]:
            state = await transition(state, services=services)
        return state

    await app.publish()

    # ORD-001: payment ok, inventory ok → COMPLETED
    r1 = await app.process_order(order_id="ORD-001").wait_result()
    assert r1["current_state"] == "COMPLETED"

    # ORD-002: payment ok, inventory out-of-stock → FAILED
    r2 = await app.process_order(order_id="ORD-002").wait_result()
    assert r2["current_state"] == "FAILED"

    # ORD-003: payment declined → FAILED (short-circuit, no inventory check)
    r3 = await app.process_order(order_id="ORD-003").wait_result()
    assert r3["current_state"] == "FAILED"
    assert not any(t["from"] == "INVENTORY_CHECK" for t in r3["history"])

    print({
        "ORD-001": r1["current_state"],
        "ORD-002": r2["current_state"],
        "ORD-003": r3["current_state"],
    })


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
