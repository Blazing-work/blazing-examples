"""
# Daily Report Generation

Scheduled job to generate and distribute daily reports via email.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Intermediate
- **Time**: 25 min
- **Tags**: scheduled, reports, automation, email

## Description

Scheduled job to generate and distribute daily reports via email.

## What you'll learn

- Scheduled workflow patterns
- Report generation from metrics
- Automated email distribution
"""

    import asyncio

from blazing import Blazing

async def main():
    app = Blazing()  # Uses Blazing SaaS by default

    @app.step
    async def fetch_daily_metrics(date: str, services=None):
        """Fetch metrics for date."""
        metrics = await services['MetricsDatabase'].get_by_date(date)

        return {
            "date": date,
            "total_orders": metrics['order_count'],
            "revenue": metrics['revenue'],
            "active_users": metrics['active_users']
        }

    @app.step
    async def generate_report(metrics: dict, services=None):
        """Generate report from metrics."""
        report = f"""
        Daily Report - {metrics['date']}
        ================================
        Total Orders: {metrics['total_orders']}
        Revenue: ${metrics['revenue']:,.2f}
        Active Users: {metrics['active_users']}
        """
        return report

    @app.step
    async def distribute_report(report: str, recipients: list, services=None):
        """Email report to recipients."""
        tasks = [
            services['EmailService'].send(email, "Daily Report", report)
            for email in recipients
        ]
        await asyncio.gather(*tasks)
        return {"sent_to": len(recipients)}

    @app.workflow
    async def daily_report_job(date: str, services=None):
        """Generate and send daily report."""
        metrics = await fetch_daily_metrics(date, services=services)
        report = await generate_report(metrics, services=services)

        recipients = await services['ConfigService'].get('report_recipients')
        result = await distribute_report(report, recipients, services=services)

        return {"date": date, "recipients": result['sent_to']}

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
