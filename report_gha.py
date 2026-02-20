#!/usr/bin/env python3
"""
report_gha.py -- GitHub Actions step summary reporter for smoke_runner.py results.

Usage:
    python report_gha.py [--results smoke_results.jsonl]

Reads: JSONL file from smoke_runner.py
Writes: Markdown table to $GITHUB_STEP_SUMMARY

Each row: example ID | status emoji | duration | error snippet (if fail)
Aggregate: total pass / skip / fail counts, overall result
"""

import argparse
import json
import os
import sys
from pathlib import Path

STATUS_EMOJI = {
    "pass": "✅",
    "skip": "⏭️",
    "fail": "❌",
}


def load_results(results_file: str) -> list:
    results = []
    with open(results_file) as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return sorted(results, key=lambda r: r["id"])


def write_summary(results: list, output_path: str):
    passed  = sum(1 for r in results if r["status"] == "pass")
    skipped = sum(1 for r in results if r["status"] == "skip")
    failed  = sum(1 for r in results if r["status"] == "fail")
    total   = len(results)

    overall = "PASSED" if failed == 0 else "FAILED"
    overall_emoji = "✅" if failed == 0 else "❌"

    lines = []
    lines.append(f"## Smoke Gate: {overall_emoji} {overall}")
    lines.append("")
    lines.append(f"**{total} examples** -- {passed} passed · {skipped} skipped · {failed} failed")
    lines.append("")

    # Failed examples first (most important)
    if failed > 0:
        lines.append("### Failed Examples")
        lines.append("")
        lines.append("| Example | Duration | Error |")
        lines.append("|---------|----------|-------|")
        for r in results:
            if r["status"] == "fail":
                error_snippet = (r.get("error") or "")[:120].replace("|", "\\|").replace("\n", " ")
                lines.append(f"| `{r['id']}` | {r['duration_s']:.1f}s | {error_snippet} |")
        lines.append("")

    # Full results table
    lines.append("### All Results")
    lines.append("")
    lines.append("| Status | Example | Duration |")
    lines.append("|--------|---------|----------|")
    for r in results:
        emoji = STATUS_EMOJI.get(r["status"], "?")
        lines.append(f"| {emoji} | `{r['id']}` | {r['duration_s']:.1f}s |")
    lines.append("")

    with open(output_path, "a") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Summary written to: {output_path}")
    print(f"Result: {overall} ({passed}/{total} passed, {skipped} skipped, {failed} failed)")


def main():
    parser = argparse.ArgumentParser(description="Write GHA step summary from smoke_runner.py results")
    parser.add_argument(
        "--results",
        default=os.environ.get("SMOKE_RESULTS_FILE", str(Path(__file__).parent / "smoke_results.jsonl")),
        help="Path to JSONL results file from smoke_runner.py",
    )
    args = parser.parse_args()

    if not Path(args.results).exists():
        print(f"ERROR: Results file not found: {args.results}", file=sys.stderr)
        sys.exit(1)

    results = load_results(args.results)

    # Write to GHA step summary if available, else stdout
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        write_summary(results, summary_path)
    else:
        # Local dev: write to stdout as preview
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            write_summary(results, tmp.name)
            print(f"(No GITHUB_STEP_SUMMARY set -- preview written to {tmp.name})")

    # Exit 1 if any failure (so GHA job fails on smoke failures)
    failed = sum(1 for r in results if r["status"] == "fail")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
