"""
# Stripe Payment Webhook

Handle Stripe payment webhooks with signature verification.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 30 min
- **Tags**: webhook, stripe, payments, events

## Description

Handle Stripe payment webhooks with signature verification.

## What you'll learn

- Stripe webhook signature verification
- Processing payment intent events
- Order fulfillment workflow patterns
"""

    import stripe

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def verify_stripe_signature(payload: str, signature: str, services=None):
        """Verify Stripe webhook signature."""
        endpoint_secret = await services['ConfigService'].get('stripe_webhook_secret')
        try:
            event = stripe.Webhook.construct_event(payload, signature, endpoint_secret)
            return event
        except ValueError:
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise ValueError("Invalid signature")

    @app.step
    async def handle_payment_success(payment_intent: dict, services=None):
        """Handle successful payment."""
        order_id = payment_intent['metadata']['order_id']
        await services['OrderDatabase'].mark_paid(order_id)
        await services['EmailService'].send_receipt(payment_intent['receipt_email'])
        return {"order_id": order_id, "status": "paid"}

    @app.workflow
    async def process_stripe_webhook(payload: str, signature: str, services=None):
        """Process Stripe webhook event."""
        event = await verify_stripe_signature(payload, signature, services=services)

        if event['type'] == 'payment_intent.succeeded':
            result = await handle_payment_success(event['data']['object'], services=services)

        return result

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
