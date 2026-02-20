#!/usr/bin/env python3
"""SEO transformation script for blazing-examples meta.json files.

Adds `technologies` field, enriches tags, and improves descriptions.
Idempotent — safe to run multiple times.
"""
import ast, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent

# ── Canonical technology display names ────────────────────────────────────────
# Maps lowercase keys (from imports/tags/ids) → display name for technologies[]
TECH_DISPLAY = {
    # AI / LLM
    "langchain": "LangChain", "langchain_core": "LangChain", "langchain_community": "LangChain",
    "langgraph": "LangGraph",
    "langblaze": "LangBlaze",
    "deepagents": "DeepAgents",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "whisper": "Whisper",
    "sentence_transformers": "Sentence Transformers",
    "transformers": "Hugging Face Transformers",
    "chromadb": "ChromaDB",
    "tiktoken": "tiktoken",
    # ML / Compute
    "torch": "PyTorch", "pytorch": "PyTorch",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "duckdb": "DuckDB",
    "pyarrow": "Apache Arrow",
    "rasterio": "Rasterio",
    # Web frameworks
    "fastapi": "FastAPI",
    "flask": "Flask",
    "quart": "Quart",
    "sanic": "Sanic",
    "litestar": "Litestar",
    "falcon": "Falcon",
    "django": "Django",
    "uvicorn": "uvicorn",
    "httpx": "HTTPX",
    "aiohttp": "aiohttp",
    # Infra / Storage
    "redis": "Redis",
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "s3": "AWS S3", "aws-s3": "AWS S3", "boto3": "AWS S3",
    "kafka": "Kafka",
    "docker": "Docker",
    "arrow": "Apache Arrow", "arrow-flight": "Apache Arrow Flight",
    # Security / Auth
    "jwt": "JWT",
    "oauth": "OAuth",
    # Sandbox / WASM
    "pyodide": "Pyodide",
    "wasm": "WebAssembly", "pyodide-wasm": "Pyodide",
    # Media
    "pdfplumber": "pdfplumber",
    "bs4": "Beautiful Soup",
    "trafilatura": "Trafilatura",
    "audio_ffmpeg": "FFmpeg",
}

# ── Tag slug → tech display (for extracting from existing tags) ───────────────
TAG_TO_DISPLAY = {k: v for k, v in TECH_DISPLAY.items()}
TAG_TO_DISPLAY.update({
    "rag": "RAG",
    "websocket": "WebSocket", "websockets": "WebSocket",
    "grpc": "gRPC",
    "graphql": "GraphQL",
})

# ── Tags to REMOVE (too generic, no search value) ────────────────────────────
REMOVE_TAGS = {
    "step", "basics", "basic", "simple", "data", "ml",
    "run_sync", "callable", "workflows", "version-pins", "syncblazing",
    "wait_result_sync", "run-sync", "depth-tracking",
}

# ── Domain/use-case tags to KEEP (good SEO, not tech-specific) ───────────────
GOOD_DOMAIN_TAGS = {
    "streaming", "rag", "etl", "auth", "distributed", "gpu", "api",
    "workflow", "sandbox", "security", "realtime", "real-time",
    "concurrency", "async", "asyncio", "pipeline", "orchestration",
    "websocket", "rest", "http", "grpc", "arrow", "inference",
    "embedding", "vector-search", "ocr", "transcription", "image-processing",
    "batch", "parallel", "scheduler", "queue", "pub-sub", "events",
    "error-handling", "retry", "timeout", "secrets", "connectors",
    "volume", "file-storage", "metrics", "monitoring", "depth-tracking",
    "dynamic-code", "signing", "isolation", "worker-types", "autoscaling",
    "serialization", "snapshot", "checkpoint", "multi-tenant",
    "state-machine", "loop", "feedback", "egress", "firewall",
}


def get_imports(flow_path: pathlib.Path) -> set:
    """Extract top-level module names from flow.py imports."""
    if not flow_path.exists():
        return set()
    try:
        tree = ast.parse(flow_path.read_text())
    except SyntaxError:
        return set()
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0].lower())
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0].lower())
    return imports


def extract_technologies(imports: set, tags: list, example_id: str, description: str) -> list:
    """Build a deduplicated list of properly-cased technology names."""
    techs = set()
    # From imports
    for imp in imports:
        if imp in TECH_DISPLAY:
            techs.add(TECH_DISPLAY[imp])
    # From existing tags
    for tag in tags:
        key = tag.lower().replace(" ", "-")
        if key in TAG_TO_DISPLAY:
            techs.add(TAG_TO_DISPLAY[key])
    # From id (e.g., 'fastapi_streaming' → FastAPI)
    id_lower = example_id.lower()
    for key, display in TECH_DISPLAY.items():
        if key in id_lower.replace("_", "-").split("-") or key in id_lower:
            techs.add(display)
    # From description
    desc_lower = description.lower()
    for key, display in TECH_DISPLAY.items():
        if len(key) > 4 and key in desc_lower:
            techs.add(display)
    # Remove Blazing itself and stdlib noise
    techs.discard("blazing")
    techs.discard("asyncio")
    techs.discard("os")
    # If uvicorn present, assume FastAPI (they're coupled in all web endpoint examples)
    if "uvicorn" in imports and ("fastapi" in id_lower or "endpoint" in id_lower or "web" in id_lower):
        techs.add("FastAPI")
    return sorted(techs)


def enrich_tags(existing_tags: list, technologies: list, example_id: str) -> list:
    """Build 5-8 SEO-optimized lowercase-slug tags."""
    tag_set = set()
    # Convert technologies → lowercase slugs
    for tech in technologies:
        slug = tech.lower().replace(" ", "-")
        tag_set.add(slug)
    # Keep good domain tags from existing
    for tag in existing_tags:
        t = tag.lower().strip()
        if t in GOOD_DOMAIN_TAGS or any(t.startswith(g) for g in ("fastapi", "pytorch", "langchain", "redis", "openai", "anthropic")):
            tag_set.add(t)
        if t not in REMOVE_TAGS and len(t) > 3 and "-" in t:
            tag_set.add(t)  # keep compound tags like 'error-handling', 'worker-types'
    # Remove generic noise
    tag_set -= REMOVE_TAGS
    # Trim to 8 max (prefer tech-specific)
    tag_list = sorted(tag_set)
    if len(tag_list) > 8:
        # Prioritize: tech tags first, then domain tags
        tech_slugs = {t.lower().replace(" ", "-") for t in technologies}
        priority = [t for t in tag_list if t in tech_slugs]
        rest = [t for t in tag_list if t not in tech_slugs]
        tag_list = (priority + rest)[:8]
    # Ensure at least 4 tags
    if len(tag_list) < 4:
        # Add 'python' and 'distributed' as baseline
        for fallback in ["python", "distributed", "blazing-flow", "async"]:
            if fallback not in tag_list:
                tag_list.append(fallback)
            if len(tag_list) >= 4:
                break
    return sorted(tag_list)


def improve_description(description: str, technologies: list, title: str, example_id: str) -> str:
    """Improve description if it's too short or doesn't mention technologies."""
    tech_mentioned = any(t.lower() in description.lower() for t in technologies if len(t) > 3)
    if len(description) >= 120 and tech_mentioned:
        return description  # already good
    # Too short or no tech mention — append tech context
    if technologies and not tech_mentioned:
        tech_str = ", ".join(technologies[:3])
        if len(description) > 80:
            return description.rstrip(".") + f" — uses {tech_str}."
        else:
            return description.rstrip(".") + f" Built with {tech_str} on Blazing Flow's distributed worker infrastructure."
    if len(description) < 80:
        return description.rstrip(".") + " — demonstrates Blazing Flow's distributed step execution model with typed inputs and structured outputs."
    return description


def transform_example(meta_path: pathlib.Path, stats: dict) -> bool:
    """Transform a single meta.json. Returns True if modified."""
    flow_path = meta_path.parent / "flow.py"
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError as e:
        print(f"  ERROR: {meta_path}: {e}")
        return False

    original = json.dumps(meta, sort_keys=True)

    imports = get_imports(flow_path)
    existing_tags = meta.get("tags", [])
    description = meta.get("description", "")
    example_id = meta.get("id", meta_path.parent.name)

    # Build technologies
    technologies = extract_technologies(imports, existing_tags, example_id, description)
    # Enrich tags
    new_tags = enrich_tags(existing_tags, technologies, example_id)
    # Improve description
    new_description = improve_description(description, technologies, meta.get("title", ""), example_id)

    # Apply
    meta["technologies"] = technologies
    meta["tags"] = new_tags
    meta["description"] = new_description

    new_str = json.dumps(meta, sort_keys=True)
    if new_str == original:
        return False

    # Write with pretty formatting, preserving field order
    ordered = {
        "id": meta.get("id"),
        "title": meta.get("title"),
        "description": meta.get("description"),
        "tags": meta.get("tags"),
        "technologies": meta.get("technologies"),
        "category": meta.get("category"),
        "difficulty": meta.get("difficulty"),
        "time": meta.get("time"),
        "products": meta.get("products"),
        "primaryProduct": meta.get("primaryProduct"),
    }
    meta_path.write_text(json.dumps(ordered, indent=2) + "\n")

    if technologies and "technologies" not in original:
        stats["technologies_added"] += 1
    if new_tags != existing_tags:
        stats["tags_enriched"] += 1
    if new_description != description:
        stats["descriptions_improved"] += 1
    return True


def main():
    stats = {"technologies_added": 0, "tags_enriched": 0, "descriptions_improved": 0, "errors": 0}
    meta_files = sorted(ROOT.glob("*/*/meta.json"))
    print(f"Processing {len(meta_files)} meta.json files...")
    modified = 0
    for path in meta_files:
        changed = transform_example(path, stats)
        if changed:
            modified += 1
    print(f"\n✓ Modified: {modified}/{len(meta_files)} files")
    print(f"  technologies field added: {stats['technologies_added']}")
    print(f"  tags enriched:            {stats['tags_enriched']}")
    print(f"  descriptions improved:    {stats['descriptions_improved']}")
    print(f"  errors:                   {stats['errors']}")

    # Validate
    print("\nValidating...")
    ids_seen = set()
    errors = []
    for path in meta_files:
        try:
            meta = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{path}: JSON parse error: {e}")
            continue
        required = ["id", "title", "description", "tags", "category", "difficulty", "time", "products", "primaryProduct", "technologies"]
        for field in required:
            if field not in meta:
                errors.append(f"{path}: missing field '{field}'")
        if meta.get("id") in ids_seen:
            errors.append(f"{path}: duplicate id '{meta['id']}'")
        ids_seen.add(meta.get("id"))
        tag_count = len(meta.get("tags", []))
        if tag_count < 4 or tag_count > 8:
            print(f"  WARN: {meta['id']} has {tag_count} tags")
    if errors:
        print(f"\n✗ Validation errors:")
        for e in errors: print(f"  {e}")
        sys.exit(1)
    else:
        print(f"✓ All {len(meta_files)} meta.json files valid")

if __name__ == "__main__":
    main()
