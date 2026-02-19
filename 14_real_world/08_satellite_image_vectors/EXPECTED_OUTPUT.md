# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- GeoTIFF satellite image file (or S3 path)
- MongoDB connection string with geospatial 2dsphere index
- `MONGODB_URI` environment variable
- Running Blazing infrastructure: `docker-compose up -d`

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - SatelliteVectors - Loading Clay foundation model (or sentence-transformers fallback)
INFO - SatelliteVectors - Processing GeoTIFF: sentinel2_tile.tif (4096x4096 pixels)
INFO - SatelliteVectors - Extracted 256 tiles (256x256 pixels each)
INFO - SatelliteVectors - Generated 256 embeddings (768-dim)
INFO - SatelliteVectors - Stored 256 vectors with GeoJSON coordinates in MongoDB
{"tiles_processed": 256, "embeddings_dim": 768, "bbox": [-122.5, 37.5, -121.9, 38.1]}
```

## Notes

- Output depends on the input GeoTIFF dimensions and spatial coverage
- Clay model produces 768-dimensional embeddings; sentence-transformers fallback may differ
- GeoJSON coordinates are `[longitude, latitude]` in WGS84 (EPSG:4326) — required for MongoDB 2dsphere
- Tile count = `(image_width / 256) * (image_height / 256)` for a 4096x4096 image = 256 tiles
