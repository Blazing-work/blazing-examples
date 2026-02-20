#!/usr/bin/env python3
"""
smoke_runner.py -- Parallel smoke test runner for all 137 blazing-examples.

Usage:
    BLAZING_API_URL=http://canary-external-url:8000 \
    BLAZING_API_TOKEN=my-token \
    python smoke_runner.py [--examples-dir /path/to/blazing-examples] [--workers 20] [--timeout 120]

Output:
    Writes JSONL to $SMOKE_RESULTS_FILE (default: smoke_results.jsonl)
    Each line: {"id": "...", "status": "pass|skip|fail", "duration_s": 1.23, "error": "..."}

Exit code:
    0 if all non-skipped examples pass
    1 if any example fails
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Technologies in meta.json that require external API keys
# Key = technology name in meta.json, Value = env var that must be set for the test to run
EXTERNAL_API_TECHNOLOGIES = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "slack": "SLACK_BOT_TOKEN",
    "discord": "DISCORD_BOT_TOKEN",
    "google-sheets": "GOOGLE_SHEETS_CREDENTIALS",
    "algolia": "ALGOLIA_API_KEY",
    "mongodb": "MONGODB_URI",
    "stripe": "STRIPE_API_KEY",
    "sendgrid": "SENDGRID_API_KEY",
    "twilio": "TWILIO_AUTH_TOKEN",
}

# Patterns in flow.py that indicate a long-running HTTP server -- these examples never exit
# and would always hit the subprocess timeout, producing false FAIL results.
# Detected before execution; skipped with reason "SKIP: server example (never exits)".
SERVER_PATTERNS = [
    "uvicorn.run(",
    "app.run(host=",
    "app.run(port=",
    ".run(host=",
    "serve(",
    "run_server(",
    "start_server(",
]


def find_examples(examples_dir: Path) -> list:
    """Discover all flow.py files (one per example)."""
    return sorted(examples_dir.glob("*/*/flow.py")) + sorted(
        p for p in examples_dir.glob("*/flow.py")
        if not any(p.parent.name.startswith(d) for d in ["__", "."])
    )


def is_server_example(flow_py: Path) -> bool:
    """Return True if flow.py contains a long-running server pattern that never exits."""
    try:
        content = flow_py.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return any(pattern in content for pattern in SERVER_PATTERNS)


def check_skip(example_dir: Path, flow_py: Path) -> tuple:
    """
    Return (should_skip, reason) based on:
    1. meta.json technologies field (external API keys)
    2. flow.py content scan (server patterns that never exit)
    """
    # Check for server patterns first (no external call needed)
    if is_server_example(flow_py):
        return True, "SKIP: server example (never exits -- uvicorn/serve/app.run pattern detected)"

    # Check for missing external API keys via meta.json
    meta_path = example_dir / "meta.json"
    if not meta_path.exists():
        return False, ""
    try:
        meta = json.loads(meta_path.read_text())
    except (json.JSONDecodeError, OSError):
        return False, ""

    technologies = [t.lower() for t in meta.get("technologies", [])]
    for tech, env_var in EXTERNAL_API_TECHNOLOGIES.items():
        if tech in technologies and not os.environ.get(env_var):
            return True, f"SKIP: {tech} requires {env_var} (not set)"
    return False, ""


def run_example(flow_py: Path, api_url: str, api_token: str, timeout: int) -> dict:
    """Run a single example as a subprocess. Returns result dict."""
    # Build example ID: category/example_name or just example_name for top-level
    parent = flow_py.parent
    grandparent = parent.parent
    examples_dir = grandparent.parent

    if grandparent == examples_dir or str(grandparent).endswith("blazing-examples"):
        example_id = parent.name
    else:
        example_id = f"{grandparent.name}/{parent.name}"

    should_skip, skip_reason = check_skip(flow_py.parent, flow_py)
    if should_skip:
        return {
            "id": example_id,
            "status": "skip",
            "duration_s": 0.0,
            "error": skip_reason,
        }

    env = os.environ.copy()
    env["BLAZING_API_URL"] = api_url
    env["BLAZING_API_TOKEN"] = api_token
    # Prevent interactive prompts
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUNBUFFERED"] = "1"

    start = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, str(flow_py)],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=str(flow_py.parent),
        )
        duration = time.monotonic() - start
        if result.returncode == 0:
            return {"id": example_id, "status": "pass", "duration_s": round(duration, 2), "error": ""}
        else:
            # Trim error to last 500 chars to keep JSONL manageable
            stderr_tail = (result.stderr or result.stdout or "")[-500:]
            return {"id": example_id, "status": "fail", "duration_s": round(duration, 2), "error": stderr_tail}
    except subprocess.TimeoutExpired:
        duration = time.monotonic() - start
        return {"id": example_id, "status": "fail", "duration_s": round(duration, 2), "error": f"TIMEOUT after {timeout}s"}
    except Exception as exc:
        duration = time.monotonic() - start
        return {"id": example_id, "status": "fail", "duration_s": round(duration, 2), "error": str(exc)}


def main():
    parser = argparse.ArgumentParser(description="Parallel smoke runner for blazing-examples")
    parser.add_argument("--examples-dir", default=str(Path(__file__).parent), help="Path to blazing-examples directory")
    parser.add_argument("--workers", type=int, default=20, help="Max parallel subprocesses (default: 20)")
    parser.add_argument("--timeout", type=int, default=120, help="Per-example timeout in seconds (default: 120)")
    args = parser.parse_args()

    api_url = os.environ.get("BLAZING_API_URL", "http://localhost:8000")
    api_token = os.environ.get("BLAZING_API_TOKEN", "smoke-token")
    results_file = os.environ.get("SMOKE_RESULTS_FILE", str(Path(args.examples_dir) / "smoke_results.jsonl"))

    examples_dir = Path(args.examples_dir)
    examples = find_examples(examples_dir)

    print(f"Found {len(examples)} examples in {examples_dir}")
    print(f"API URL: {api_url} | Workers: {args.workers} | Timeout: {args.timeout}s")
    print(f"Results: {results_file}")

    results = []
    wall_start = time.monotonic()

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_example, flow_py, api_url, api_token, args.timeout): flow_py
            for flow_py in examples
        }
        for future in as_completed(futures):
            r = future.result()
            results.append(r)
            status_icon = {"pass": "PASS", "skip": "SKIP", "fail": "FAIL"}.get(r["status"], "?")
            print(f"  [{status_icon}] {r['id']} ({r['duration_s']:.1f}s)")
            if r["status"] == "fail":
                print(f"         {r['error'][:200]}")

    wall_duration = time.monotonic() - wall_start

    # Write JSONL results
    with open(results_file, "w") as f:
        for r in sorted(results, key=lambda x: x["id"]):
            f.write(json.dumps(r) + "\n")

    # Summary
    passed  = sum(1 for r in results if r["status"] == "pass")
    skipped = sum(1 for r in results if r["status"] == "skip")
    failed  = sum(1 for r in results if r["status"] == "fail")
    print(f"\n{'='*60}")
    print(f"SMOKE RESULTS: {passed} pass / {skipped} skip / {failed} fail")
    print(f"Wall time: {wall_duration:.1f}s ({wall_duration/60:.1f} min)")
    print(f"Results written to: {results_file}")

    if failed > 0:
        print(f"\nFAILED EXAMPLES:")
        for r in results:
            if r["status"] == "fail":
                print(f"  - {r['id']}: {r['error'][:200]}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
