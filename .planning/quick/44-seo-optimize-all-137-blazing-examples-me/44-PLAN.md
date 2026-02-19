---
phase: 44-seo-optimize-all-137-blazing-examples-me
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - blazing-examples/seo_transform.py
  - blazing-examples/examples.json
  - blazing-examples/*/*/meta.json
autonomous: true
requirements: []

must_haves:
  truths:
    - "All 137 meta.json files contain a `technologies` field with properly-cased library names"
    - "All 137 meta.json files have 5-8 SEO-optimized lowercase-slug tags"
    - "Descriptions are 100-220 chars and front-load recognizable tech/use-case keywords"
    - "No meta.json has id, title, category, difficulty, time, products, or primaryProduct modified"
    - "examples.json regenerated and reflects all 137 entries with updated fields"
    - "Script prints a summary of enrichment counts (tags, descriptions, technologies)"
  artifacts:
    - path: "blazing-examples/seo_transform.py"
      provides: "Idempotent transform script for all 137 meta.json files"
      exports: ["main"]
    - path: "blazing-examples/examples.json"
      provides: "Regenerated manifest with SEO-enriched metadata"
      contains: "technologies"
  key_links:
    - from: "seo_transform.py"
      to: "*/*/meta.json"
      via: "json.load / json.dump in-place per file"
      pattern: "json\\.dump.*meta_path"
    - from: "seo_transform.py"
      to: "*/*/flow.py"
      via: "import statement scanning for tech detection"
      pattern: "import.*torch|fastapi|langchain"
    - from: "seo_transform.py"
      to: "generate_manifest.py"
      via: "subprocess or direct function call after transforms complete"
      pattern: "generate_manifest|subprocess"
---

<objective>
Write, run, and validate a Python script that SEO-enriches all 137 meta.json files in blazing-examples, then regenerates examples.json.

Purpose: Make blazing-examples discoverable via search terms like "Python distributed task queue FastAPI", "run untrusted Python pyodide", "LangChain production architecture". Current tags are generic (step, basics, sync) and descriptions are short or tech-free.
Output: seo_transform.py (the transform tool), 137 updated meta.json files, regenerated examples.json.
</objective>

<execution_context>
@/Users/jonathanborduas/.claude/get-shit-done/workflows/execute-plan.md
@/Users/jonathanborduas/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@/Users/jonathanborduas/code/blazing/blazing-examples/generate_manifest.py
@/Users/jonathanborduas/code/blazing/blazing-examples/examples.json
</context>

<tasks>

<task type="auto">
  <name>Task 1: Write seo_transform.py — tech detection + tag/description/technologies enrichment</name>
  <files>blazing-examples/seo_transform.py</files>
  <action>
Create `/Users/jonathanborduas/code/blazing/blazing-examples/seo_transform.py` as a standalone Python 3 script.

The script must:

**Phase 1 — Build tech detection for each example**

For each example folder (has meta.json), scan three sources to detect which technologies are used:
1. `flow.py` import lines (if file exists) — regex `^(?:import|from)\s+(\w+)`
2. Existing `meta.json` tags — scan for tech-name substrings
3. Example `id` and `description` strings — keyword scan

Apply this canonical mapping (key = lowercase import/keyword, value = display name):
```python
TECH_MAP = {
    "torch": "PyTorch",
    "langchain_core": "LangChain",
    "langchain": "LangChain",
    "langblaze": "LangBlaze",
    "deepagents": "DeepAgents",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "quart": "Quart",
    "redis": "Redis",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "jwt": "JWT",
    "pyarrow": "Apache Arrow",
    "arrow": "Apache Arrow",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "duckdb": "DuckDB",
    "chromadb": "ChromaDB",
    "sentence_transformers": "Sentence Transformers",
    "transformers": "Hugging Face Transformers",
    "uvicorn": "uvicorn",
    "httpx": "HTTPX",
    "langgraph": "LangGraph",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "whisper": "Whisper",
    "kafka": "Kafka",
    "docker": "Docker",
    "s3": "AWS S3",
    "websocket": "WebSocket",
    "pyodide": "Pyodide",
    "wasm": "WebAssembly",
    "stripe": "Stripe",
    "github": "GitHub",
}
```

Additional scan: scan existing tag strings for lowercase versions of any TECH_MAP key.
Deduplicate display names and sort alphabetically. Result = `technologies` list.

**Phase 2 — Derive SEO slug tags**

Build tag list for each example:
1. Start from `technologies` field: map each display name to a lowercase slug:
   - "PyTorch" → "pytorch", "LangChain" → "langchain", "FastAPI" → "fastapi",
   - "AWS S3" → "aws-s3", "Sentence Transformers" → "sentence-transformers",
   - "WebAssembly" → "webassembly", "Pyodide" → "pyodide", "Apache Arrow" → "apache-arrow",
   - others: `name.lower().replace(" ", "-")`
2. Keep existing domain/concept tags that match an allowlist:
   ```python
   KEEP_TAGS = {
       "streaming", "rag", "etl", "auth", "distributed", "gpu", "ml", "api",
       "workflow", "sandbox", "security", "webhook", "agents", "inference",
       "pipeline", "realtime", "async", "batch", "cache", "queue", "sse",
       "multi-product", "a100", "h100", "local-stack", "quickstart", "python",
       "neural-network", "payments", "storage", "files", "connectors",
   }
   ```
3. Remove ultra-generic tags: "step", "basics", "data", "simple", "run_sync",
   "callable", "version-pins", "syncblazing", "wait_result_sync", "sync",
   "parallel", "task", "demo"
4. If resulting tag count < 4, derive additional domain tags from the description
   and example ID by scanning for these domain keywords: "stream", "rag", "etl",
   "auth", "distributed", "gpu", "ml", "agent", "inference", "pipeline", "cache",
   "queue", "webhook", "batch", "realtime"
5. Trim to max 8 tags (tech tags take priority, then domain tags alphabetically)

**Phase 3 — Improve descriptions**

Rewrite description if EITHER condition is true:
- `len(description) < 100`
- description does not contain any recognizable tech/use-case name from TECH_MAP values
  or these domain words: streaming, RAG, ETL, auth, distributed, GPU, ML, agent,
  inference, pipeline, sandbox, webhook, Pyodide, LangChain, etc.

When rewriting, use the example's: title, category, technologies detected, existing
description (even if short), and example ID to compose a new description.

Formula: `"[Action verb] [specific use case] with [key technologies]. [What makes it distinctive/what patterns it shows]."`

Use a lookup dict `DESCRIPTION_OVERRIDES` keyed by example ID for known-bad descriptions.
Build this dict with at least these entries:
```python
DESCRIPTION_OVERRIDES = {
    "hello_world": "Run the simplest possible Blazing Flow application with two steps and two workflows — demonstrates @app.step, @app.workflow, publish(), and wait_result() across distributed Python workers.",
    "basic_step": "Execute a single decorated Python function as a distributed step with Blazing Flow — demonstrates the @app.step decorator, type annotations, and structured return values across CPU workers.",
    "basic_task": "Define and run a basic Blazing Flow task with @app.step — shows step registration, workflow chaining, and synchronous result retrieval with wait_result().",
    "stripe_webhook": "Verify and process Stripe payment webhooks with HMAC-SHA256 signature validation in a distributed Blazing Flow workflow — routes payment_intent.succeeded events to fulfillment and receipt steps.",
    "ml_inference_pipeline": "Deploy ML models with Blazing Core infrastructure and orchestrate inference across Blazing Flow steps — combines model loading, prediction, and result collection in a multi-product pipeline.",
}
```
For all other examples that need rewriting (condition above): construct description
programmatically from title + technologies + category + short existing description.
Template: `f"{title} with {' and '.join(technologies[:2]) if technologies else category} — {existing_desc_trimmed}"`
Cap at 220 chars, ensure >= 100 chars by appending category context if needed.

**Phase 4 — Write meta.json files in-place**

For each meta.json:
- Load existing JSON
- DO NOT modify: id, title, category, difficulty, time, products, primaryProduct
- Set: technologies (new field), tags (replaced), description (replaced if improved)
- Write back with `json.dump(data, f, indent=2, ensure_ascii=False)` + trailing newline

**Phase 5 — Print summary**

```
SEO Transform Complete
======================
Examples processed: 137
Technologies field added: N
Tags enriched: N (had < 4 or no tech tags)
Descriptions improved: N (were < 100 chars or tech-free)

Top technologies detected:
  FastAPI: 5
  PyTorch: 3
  ...
```

Validation checks (print WARN if any fail):
- All 137 meta.json parse as valid JSON
- No meta.json has fewer than 4 tags or more than 8 tags
- No meta.json is missing the `technologies` field
- No id/title/products/primaryProduct was changed (compare before/after)

Script must be idempotent (safe to run twice).
  </action>
  <verify>
Run: `cd /Users/jonathanborduas/code/blazing/blazing-examples && python3 seo_transform.py`
Expected: prints summary with 137 processed, no WARN lines, tag counts 4-8 for all examples.
Spot-check: `python3 -c "import json; m=json.load(open('01_getting_started/hello_world/meta.json')); print(m['technologies'], m['tags'], len(m['description']))"`
Expected: technologies is a non-empty list, tags has 4-8 items, description >= 100 chars.
  </verify>
  <done>
Script runs without errors, prints 137 processed, all meta.json files have `technologies` array, 4-8 tags each, and descriptions >= 100 chars. No protected fields (id, products, primaryProduct) were altered.
  </done>
</task>

<task type="auto">
  <name>Task 2: Validate all 137 files and regenerate examples.json</name>
  <files>blazing-examples/examples.json</files>
  <action>
Run validation and manifest regeneration:

**Validation script (run inline, not a file):**
```python
import json
from pathlib import Path

repo = Path("/Users/jonathanborduas/code/blazing/blazing-examples")
meta_files = list(repo.rglob("meta.json"))
errors = []
for f in meta_files:
    try:
        m = json.loads(f.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON: {f} — {e}")
        continue
    tags = m.get("tags", [])
    if not 4 <= len(tags) <= 8:
        errors.append(f"TAG COUNT {len(tags)}: {f.parent.name} tags={tags}")
    if "technologies" not in m:
        errors.append(f"MISSING technologies: {f.parent.name}")
    if len(m.get("description","")) < 80:
        errors.append(f"SHORT DESC ({len(m.get('description',''))} chars): {f.parent.name}")

print(f"Validated {len(meta_files)} meta.json files")
if errors:
    for e in errors:
        print("  ERROR:", e)
else:
    print("  All checks passed")
```

Run: `python3 -c "<above>"` — fix any errors by updating `seo_transform.py` DESCRIPTION_OVERRIDES or KEEP_TAGS and re-running.

**Regenerate examples.json:**
Run: `cd /Users/jonathanborduas/code/blazing/blazing-examples && python3 generate_manifest.py`

Verify examples.json:
```bash
python3 -c "
import json
ex = json.load(open('/Users/jonathanborduas/code/blazing/blazing-examples/examples.json'))
print(f'Total examples: {len(ex)}')
has_tech = sum(1 for e in ex if e.get('technologies'))
print(f'With technologies field: {has_tech}')
print('First:', ex[0].get('id'), ex[0].get('technologies'))
"
```
Expected: 137 examples, all with technologies field visible in manifest.
  </action>
  <verify>
`python3 -c "import json; ex=json.load(open('/Users/jonathanborduas/code/blazing/blazing-examples/examples.json')); assert len(ex)==137, f'Got {len(ex)}'; print('OK: 137 examples in manifest')`
  </verify>
  <done>
examples.json contains exactly 137 entries. Every entry reflects updated tags, description, and technologies from meta.json. No JSON parse errors across all files.
  </done>
</task>

</tasks>

<verification>
1. `python3 -c "import json; [json.load(open(f)) for f in __import__('pathlib').Path('/Users/jonathanborduas/code/blazing/blazing-examples').rglob('meta.json')]"` — no exceptions
2. Tag count for every example: 4-8 tags
3. Spot-check 5 examples across categories confirm technologies field present
4. `wc -l examples.json` confirms file was regenerated (timestamp newer than before run)
5. `python3 generate_manifest.py` exits with code 0 and prints "Found 137 examples"
</verification>

<success_criteria>
- seo_transform.py runs idempotently and prints 137 processed with no ERRORs
- All 137 meta.json files have: technologies (array), tags (4-8 slugs with tech names), descriptions (100+ chars mentioning tech or use case)
- No protected fields altered (id, title, category, difficulty, time, products, primaryProduct)
- examples.json regenerated with 137 entries including technologies field
</success_criteria>

<output>
After completion, create `.planning/quick/44-seo-optimize-all-137-blazing-examples-me/44-01-SUMMARY.md` with:
- Files modified (list of meta.json dirs, seo_transform.py, examples.json)
- Enrichment counts (technologies added, tags enriched, descriptions improved)
- Any patterns or TECH_MAP entries added beyond the initial list
</output>
