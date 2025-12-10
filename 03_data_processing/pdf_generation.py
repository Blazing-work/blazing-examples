"""
# PDF Generation Workflow

Generate PDF documents from templates with data from multiple sources.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 35 min
- **Tags**: pdf, generation, template, file-processing

## Description

Generate PDF documents from templates with data from multiple sources.

## What you'll learn

- PDF generation with WeasyPrint
- Template rendering patterns
- Document storage and delivery
"""

from weasyprint import HTML

from blazing import Blazing


async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def generate_invoice_data(order_id: str, services=None):
        """Fetch data for invoice."""
        order = await services["OrderDatabase"].get_order(order_id)
        customer = await services["UserDatabase"].get_user(order["customer_id"])
        items = await services["OrderDatabase"].get_items(order_id)

        return {
            "order": order,
            "customer": customer,
            "items": items,
            "total": sum(item["price"] * item["qty"] for item in items),
        }

    @app.step
    async def render_pdf(data: dict, template: str, services=None):
        """Render PDF from template."""

        # Render HTML from template
        html_content = await services["TemplateService"].render(template, data)

        # Convert to PDF
        pdf_bytes = HTML(string=html_content).write_pdf()

        return pdf_bytes

    @app.step
    async def upload_invoice(order_id: str, pdf_bytes: bytes, services=None):
        """Upload invoice to storage."""
        file_key = f"invoices/{order_id}.pdf"
        await services["FileStorageService"].upload(file_key, pdf_bytes)

        # Generate signed URL
        url = await services["FileStorageService"].get_signed_url(
            file_key, expires_in=3600
        )
        return {"url": url, "file_key": file_key}

    @app.workflow
    async def create_invoice(order_id: str, services=None):
        """Generate and store invoice PDF."""
        data = await generate_invoice_data(order_id, services=services)
        pdf_bytes = await render_pdf(data, "invoice_template.html", services=services)
        result = await upload_invoice(order_id, pdf_bytes, services=services)

        return {
            "order_id": order_id,
            "invoice_url": result["url"],
            "total": data["total"],
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
