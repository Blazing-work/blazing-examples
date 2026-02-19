"""
Satellite Image Vectors Example for Blazing

Demonstrates geospatial ML pipeline with:
- GeoTIFF reading with rasterio (CRS, affine transform, bounds)
- 256x256 tile extraction from satellite imagery
- Clay foundation model embeddings (768-dim, trained on 70M satellite images)
- sentence-transformers fallback for GPU-free environments
- MongoDB 2dsphere geospatial indexing with GeoJSON
- Geospatial search via $geoNear aggregation

Production patterns:
- Load embedding model in connect() (Clay or fallback)
- Coordinate conversion via rasterio.transform.xy() (NOT manual math)
- GeoJSON [longitude, latitude] order (NOT [lat, lon])
- run_in_executor for sync model inference and rasterio operations
- 2dsphere index for efficient geospatial queries
- WGS84 CRS (EPSG:4326) required for MongoDB geospatial
"""

import os
import logging
import asyncio
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone

import numpy as np
import rasterio
from rasterio.transform import xy

from blazing import Blazing, BaseService
from blazing_service.connectors.mongodb import MongoDBConnector
from blazing_service.connectors.secrets import SecretsConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blazing app
app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=["huggingface.co"])
class SatelliteVectorService(BaseService):
    """
    Satellite image vector extraction with geospatial indexing.

    Pipeline flow:
    1. Read GeoTIFF with rasterio (extract image data + geospatial metadata)
    2. Extract 256x256 tiles in fixed grid
    3. Compute lat/lon center for each tile via rasterio.transform.xy()
    4. Generate embeddings (Clay foundation model or sentence-transformers fallback)
    5. Store in MongoDB with GeoJSON Point and 2dsphere index
    6. Search tiles by location using $geoNear aggregation

    Embedding models:
    - Clay (primary): 768-dim, trained on 70M satellite images, ~6GB GPU or slow CPU
    - sentence-transformers (fallback): 384-dim, general-purpose, CPU-friendly

    GeoTIFF requirements:
    - EPSG:4326 (WGS84) CRS for MongoDB 2dsphere compatibility
    - 3+ bands (RGB or multispectral)
    - Dimensions divisible by tile_size (256) or handle edge tiles

    CRITICAL coordinate ordering:
    - MongoDB GeoJSON requires [longitude, latitude] (NOT [lat, lon])
    - rasterio.transform.xy(row, col) returns (x, y) = (longitude, latitude) in EPSG:4326
    """

    def __init__(self, connector_instances=None):
        """Initialize satellite vector service."""
        super().__init__(connector_instances)

        # Initialize connectors
        self.secrets = connector_instances.get('secrets') if connector_instances else SecretsConnector()
        self.mongo = connector_instances.get('mongodb') if connector_instances else None

        # Embedding model (Clay or sentence-transformers)
        self.model = None
        self.model_type = None  # 'clay' or 'sentence-transformers'
        self.processor = None   # Clay processor (if Clay model loaded)

        logger.info("SatelliteVectorService initialized")

    async def connect(self):
        """
        Load embedding model on service startup.

        Tries to load Clay foundation model first (best for satellite imagery).
        Falls back to sentence-transformers if Clay unavailable (sparse docs, GPU requirements).

        Model download is heavy (~500MB-2GB), done once here.
        """
        # Ensure MongoDB connector is connected
        if self.mongo and not self.mongo.is_connected:
            await self.mongo.connect()

        # Try loading Clay model first (primary choice)
        try:
            logger.info("Attempting to load Clay foundation model from Hugging Face...")
            loop = asyncio.get_event_loop()
            self.model, self.processor = await loop.run_in_executor(
                None,
                self._load_clay_model
            )
            self.model_type = 'clay'
            logger.info("Clay foundation model loaded successfully (768-dim embeddings)")
        except Exception as e:
            logger.warning(f"Clay model failed to load: {e}")
            logger.info("Falling back to sentence-transformers (all-MiniLM-L6-v2)...")

            # Fallback to sentence-transformers
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                None,
                self._load_sentence_transformer
            )
            self.model_type = 'sentence-transformers'
            logger.info("sentence-transformers fallback loaded (384-dim embeddings)")

        logger.info("SatelliteVectorService connected")

    def _load_clay_model(self):
        """
        Load Clay foundation model synchronously.

        Clay model trained on 70M satellite images, outputs 768-dim embeddings.
        Requires transformers library and trust_remote_code=True.
        """
        from transformers import AutoModel, AutoProcessor
        import torch

        model = AutoModel.from_pretrained(
            "made-with-clay/Clay",
            trust_remote_code=True
        )
        processor = AutoProcessor.from_pretrained(
            "made-with-clay/Clay",
            trust_remote_code=True
        )

        # Move to CPU (GPU detection would check torch.cuda.is_available())
        model.to('cpu')
        # Set to evaluation mode for inference
        model.train(False)

        return model, processor

    def _load_sentence_transformer(self):
        """
        Load sentence-transformers model synchronously (fallback).

        all-MiniLM-L6-v2: 384-dim, general-purpose, works with flattened tile arrays.
        """
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model

    async def read_geotiff(
        self,
        file_path: str
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Read GeoTIFF file with rasterio.

        Extracts:
        - Image data: (bands, height, width) numpy array
        - Geospatial metadata: bounds, CRS, transform, width, height, band count

        Returns:
            (image_array, metadata_dict)
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._read_geotiff_sync,
            file_path
        )

    def _read_geotiff_sync(self, file_path: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Read GeoTIFF synchronously (rasterio is sync-only)."""
        with rasterio.open(file_path) as src:
            # Read all bands
            image = src.read()  # Shape: (bands, height, width)

            # Extract geospatial metadata
            metadata = {
                "bounds": {
                    "left": src.bounds.left,
                    "bottom": src.bounds.bottom,
                    "right": src.bounds.right,
                    "top": src.bounds.top
                },
                "crs": str(src.crs),
                "transform": src.transform,  # Affine transform object
                "width": src.width,
                "height": src.height,
                "count": src.count,  # Number of bands
                "source_file": file_path
            }

            # Verify CRS is WGS84 (required for MongoDB 2dsphere)
            if str(src.crs) != 'EPSG:4326':
                logger.warning(
                    f"GeoTIFF CRS is {src.crs}, not EPSG:4326. "
                    "Reprojection needed for MongoDB 2dsphere (out of scope for this example)."
                )

            return image, metadata

    async def extract_tiles(
        self,
        image: np.ndarray,
        metadata: Dict[str, Any],
        tile_size: int = 256,
        stride: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract fixed-size tiles from satellite image.

        For each tile:
        - Slice numpy array
        - Compute center lat/lon via rasterio.transform.xy()
        - Return tile array + metadata

        Args:
            image: Image array (bands, height, width)
            metadata: Metadata dict with 'transform' key
            tile_size: Tile dimension in pixels (256x256 standard)
            stride: Stride for sliding window (default: tile_size for no overlap)

        Returns:
            List of dicts: {tile_array, tile_position: {row, col}, center: {lon, lat}}
        """
        if stride is None:
            stride = tile_size

        bands, height, width = image.shape
        tiles = []

        transform = metadata['transform']

        for row in range(0, height - tile_size + 1, stride):
            for col in range(0, width - tile_size + 1, stride):
                # Extract tile
                tile_array = image[:, row:row+tile_size, col:col+tile_size]

                # Compute center pixel coordinates (row + tile_size//2, col + tile_size//2)
                center_row = row + tile_size // 2
                center_col = col + tile_size // 2

                # Convert pixel coordinates to lat/lon using rasterio.transform.xy()
                # xy(row, col, transform) returns (x, y) where x=longitude, y=latitude in EPSG:4326
                lon, lat = xy(transform, center_row, center_col)

                tiles.append({
                    "tile_array": tile_array,
                    "tile_position": {"row": int(row), "col": int(col)},
                    "center": {"lon": float(lon), "lat": float(lat)}
                })

        logger.info(f"Extracted {len(tiles)} tiles ({tile_size}x{tile_size}) from image")
        return tiles

    async def embed_tiles(
        self,
        tiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for tiles using loaded model.

        Clay model path: Preprocess RGB tiles, generate 768-dim embeddings
        Fallback path: Flatten tile to 1D, normalize, embed with sentence-transformers

        All inference wrapped in run_in_executor (sync operations).

        Returns:
            Tiles with added 'embedding' field
        """
        loop = asyncio.get_event_loop()

        for tile in tiles:
            tile_array = tile['tile_array']

            if self.model_type == 'clay':
                # Clay model embedding
                embedding = await loop.run_in_executor(
                    None,
                    self._embed_tile_clay,
                    tile_array
                )
            else:
                # sentence-transformers fallback
                embedding = await loop.run_in_executor(
                    None,
                    self._embed_tile_sentence_transformer,
                    tile_array
                )

            tile['embedding'] = embedding
            # Remove tile_array to reduce memory (not needed after embedding)
            del tile['tile_array']

        logger.info(f"Generated embeddings for {len(tiles)} tiles ({self.model_type})")
        return tiles

    def _embed_tile_clay(self, tile_array: np.ndarray) -> List[float]:
        """
        Generate Clay embedding synchronously.

        Clay expects RGB image in (height, width, channels) format.
        """
        import torch

        # Convert from (bands, height, width) to (height, width, bands)
        tile_rgb = np.transpose(tile_array[:3], (1, 2, 0))

        # Normalize to [0, 1] (uint8 -> float32)
        tile_rgb = tile_rgb.astype(np.float32) / 255.0

        # Preprocess with Clay processor
        inputs = self.processor(images=tile_rgb, return_tensors="pt")

        # Generate embedding (no gradient computation)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Clay outputs last_hidden_state, take mean across spatial dimensions
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze()

        return embedding.cpu().numpy().tolist()

    def _embed_tile_sentence_transformer(self, tile_array: np.ndarray) -> List[float]:
        """
        Generate sentence-transformers embedding synchronously (fallback).

        Flatten tile to 1D array, normalize, encode.
        """
        # Flatten to 1D (bands * height * width)
        tile_flat = tile_array.flatten()

        # Normalize to [0, 1]
        tile_normalized = tile_flat.astype(np.float32) / 255.0

        # Convert to string representation for sentence-transformers
        # (sentence-transformers expects text, but we can encode numeric arrays too)
        # Alternative: Use CLIP or other vision models, but sentence-transformers is the fallback
        tile_str = ' '.join(map(str, tile_normalized[:1000]))  # Limit length to avoid issues

        # Generate embedding
        embedding = self.model.encode(tile_str, convert_to_numpy=True)

        return embedding.tolist()

    async def store_with_geospatial_index(
        self,
        collection: str,
        tiles: List[Dict[str, Any]],
        metadata: Dict[str, Any]
    ) -> int:
        """
        Store tile embeddings in MongoDB with 2dsphere geospatial index.

        MongoDB 2dsphere index requirements:
        - GeoJSON Point format: {"type": "Point", "coordinates": [longitude, latitude]}
        - Coordinates order: [longitude, latitude] (NOT [lat, lon])
        - WGS84 CRS (EPSG:4326)

        Returns:
            Number of tiles stored
        """
        # Create 2dsphere index on location field (idempotent)
        coll = self.mongo._get_collection(collection)
        await coll.create_index([("location", "2dsphere")])
        logger.info(f"Created 2dsphere index on '{collection}.location'")

        # Insert tiles
        count = 0
        for tile in tiles:
            # Create MongoDB document with GeoJSON location
            document = {
                "embedding": tile['embedding'],
                "location": {
                    "type": "Point",
                    "coordinates": [tile['center']['lon'], tile['center']['lat']]  # [lon, lat]
                },
                "tile_position": tile['tile_position'],
                "source_image": metadata['source_file'],
                "crs": metadata['crs'],
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            await self.mongo.insert(collection=collection, document=document)
            count += 1

        logger.info(f"Stored {count} tiles in '{collection}' with geospatial index")
        return count

    async def search_by_location(
        self,
        collection: str,
        longitude: float,
        latitude: float,
        radius_meters: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Search for tiles near a geographic location using 2dsphere index.

        MongoDB $geoNear aggregation pipeline with spherical geometry.

        Args:
            collection: MongoDB collection name
            longitude: Query longitude (e.g., -122.4194 for SF)
            latitude: Query latitude (e.g., 37.7749 for SF)
            radius_meters: Search radius in meters (default: 1000m = 1km)

        Returns:
            List of tiles sorted by distance (nearest first)
        """
        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]  # [lon, lat]
                    },
                    "distanceField": "distance",
                    "maxDistance": radius_meters,
                    "spherical": True
                }
            },
            {"$limit": 10}
        ]

        results = await self.mongo.aggregate(
            collection=collection,
            pipeline=pipeline
        )

        logger.info(f"Found {len(results)} tiles within {radius_meters}m of ({longitude}, {latitude})")
        return results

    async def process_geotiff(
        self,
        file_path: str,
        collection: str,
        tile_size: int = 256
    ) -> Dict[str, Any]:
        """
        Full pipeline: read GeoTIFF → extract tiles → embed → store with geospatial index.

        Args:
            file_path: Path to GeoTIFF file
            collection: MongoDB collection name for storage
            tile_size: Tile dimension in pixels (default: 256)

        Returns:
            Stats dict with tiles_extracted, tiles_stored, source_file, bounds
        """
        logger.info(f"Processing GeoTIFF: {file_path}")

        # Read GeoTIFF
        image, metadata = await self.read_geotiff(file_path)

        # Extract tiles
        tiles = await self.extract_tiles(
            image=image,
            metadata=metadata,
            tile_size=tile_size
        )

        # Generate embeddings
        tiles_with_embeddings = await self.embed_tiles(tiles=tiles)

        # Store in MongoDB with 2dsphere index
        stored = await self.store_with_geospatial_index(
            collection=collection,
            tiles=tiles_with_embeddings,
            metadata=metadata
        )

        return {
            "tiles_extracted": len(tiles),
            "tiles_stored": stored,
            "source_file": file_path,
            "bounds": metadata['bounds'],
            "crs": metadata['crs'],
            "model_type": self.model_type
        }


# Endpoints

@app.endpoint.post("/satellite/process")
async def process_satellite_image(request, services=None):
    """
    Process satellite image: extract tiles, generate embeddings, store with geospatial index.

    Body: {
        "file_path": "./examples/24-satellite-image-vectors/sample_satellite.tif",
        "collection": "satellite_tiles",
        "tile_size": 256
    }

    Response: {
        "tiles_extracted": 4,
        "tiles_stored": 4,
        "source_file": "...",
        "bounds": {...},
        "crs": "EPSG:4326",
        "model_type": "clay" | "sentence-transformers"
    }
    """
    body = await request.json()
    service = services['SatelliteVectorService']

    stats = await service.process_geotiff(
        file_path=body['file_path'],
        collection=body['collection'],
        tile_size=body.get('tile_size', 256)
    )

    return stats


@app.endpoint.post("/satellite/search")
async def search_satellite_tiles(request, services=None):
    """
    Search for satellite tiles by location (geospatial query).

    Body: {
        "collection": "satellite_tiles",
        "longitude": -122.4194,
        "latitude": 37.7749,
        "radius_meters": 5000
    }

    Response: {
        "results": [
            {
                "_id": "...",
                "location": {"type": "Point", "coordinates": [-122.42, 37.77]},
                "tile_position": {"row": 0, "col": 0},
                "embedding": [...],
                "distance": 120.5,  // meters from query point
                "source_image": "...",
                "created_at": "2026-02-06T..."
            },
            ...
        ],
        "count": 3
    }
    """
    body = await request.json()
    service = services['SatelliteVectorService']

    results = await service.search_by_location(
        collection=body['collection'],
        longitude=body['longitude'],
        latitude=body['latitude'],
        radius_meters=body.get('radius_meters', 1000)
    )

    return {"results": results, "count": len(results)}


@app.endpoint.get("/satellite/tiles")
async def list_satellite_tiles(request, services=None):
    """
    List all stored satellite tiles in collection.

    Query params: ?collection=satellite_tiles&limit=20

    Response: {
        "tiles": [
            {
                "_id": "...",
                "location": {...},
                "tile_position": {...},
                "source_image": "...",
                "created_at": "..."
            },
            ...
        ],
        "count": 20
    }
    """
    collection = request.query_params.get('collection', 'satellite_tiles')
    limit = int(request.query_params.get('limit', 20))

    service = services['SatelliteVectorService']

    tiles = await service.mongo.find(
        collection=collection,
        filter={},
        limit=limit,
        projection={"embedding": 0}  # Exclude embeddings for listing
    )

    return {"tiles": tiles, "count": len(tiles)}


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
