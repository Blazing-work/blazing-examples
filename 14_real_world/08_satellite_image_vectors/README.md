# Satellite Image Vectors

Geospatial ML pipeline: GeoTIFF → tile extraction → embeddings → MongoDB 2dsphere index.

## Patterns

- rasterio for GeoTIFF reading and affine transform coordinate conversion
- 256×256 tile extraction with center lat/lon via `rasterio.transform.xy()`
- Clay foundation model (768-dim, trained on 70M satellite images) with sentence-transformers fallback
- MongoDB GeoJSON `{"type": "Point", "coordinates": [lon, lat]}` (longitude first!)
- `$geoNear` aggregation for radius-based geospatial search

## ⚠️ GeoJSON Coordinate Order

MongoDB requires `[longitude, latitude]` (NOT `[lat, lon]`). rasterio's `xy()` returns `(x, y)` = `(lon, lat)` for EPSG:4326.

## Setup

```bash
pip install rasterio numpy
```

For Clay model: `pip install transformers torch`  
GeoTIFF must be EPSG:4326 (WGS84) for MongoDB 2dsphere compatibility.

## Endpoints

- `POST /satellite/process` — process GeoTIFF
- `POST /satellite/search` — search tiles by location
- `GET /satellite/tiles` — list stored tiles
