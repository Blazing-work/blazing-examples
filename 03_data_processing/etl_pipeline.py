"""
# ETL Pipeline

Complete Extract-Transform-Load pipeline for data warehousing.

## Metadata
- **Product**: Blazing Flow
- **Difficulty**: Advanced
- **Time**: 30 min
- **Tags**: etl, pipeline, data-warehouse, workflow

## Description

Complete Extract-Transform-Load pipeline for data warehousing.

## What you'll learn

- ETL pipeline architecture
- Data extraction from sources
- Data transformation and loading
"""



from blazing import Blazing

async def main():
    app = Blazing(api_url="http://localhost:8000", api_token="your-token")

    @app.step
    async def extract(source: str, services=None):
        """Extract data from source."""
        data = await services['DataSource'].fetch(source)
        return data

    @app.step
    async def transform(data: list, services=none):
        """Transform data."""
        # Clean, normalize, enrich
        cleaned = [d for d in data if d.get('valid')]
        enriched = [
            {**d, 'processed_at': datetime.now().isoformat()}
            for d in cleaned
        ]
        return enriched

    @app.step
    async def load(data: list, destination: str, services=None):
        """Load data to destination."""
        await services['DataWarehouse'].bulk_insert(destination, data)
        return {"loaded": len(data), "destination": destination}

    @app.workflow
    async def etl_pipeline(source: str, destination: str, services=None):
        """Complete ETL pipeline."""
        raw_data = await extract(source, services=services)
        transformed = await transform(raw_data, services=services)
        result = await load(transformed, destination, services=services)
        return {
            "source": source,
            "destination": destination,
            "rows_processed": result['loaded']
        }

    await app.publish()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
