"""
validate_outputs.py — EXPECTED_OUTPUT.md existence and content check.

For each example directory, verifies that EXPECTED_OUTPUT.md:
  - Is non-empty (size > 0 bytes)
  - Contains at least one non-whitespace line

Missing EXPECTED_OUTPUT.md is reported as a WARNING (audit.py owns the MISSING check).
Empty EXPECTED_OUTPUT.md is an ERROR (this script owns the emptiness check).

Usage (from blazing-examples root):
    python3 tests/validate_outputs.py

Exit codes:
    0 — all EXPECTED_OUTPUT.md files are non-empty
    1 — one or more EXPECTED_OUTPUT.md files are empty or whitespace-only
"""

import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent


def iter_example_dirs(repo_root: pathlib.Path):
    """Yield all example directories containing meta.json."""
    for cat_dir in sorted(repo_root.glob("[0-9][0-9]_*/")):
        if not cat_dir.is_dir():
            continue
        for example_dir in sorted(cat_dir.iterdir()):
            if not example_dir.is_dir():
                continue
            if example_dir.name == "__pycache__":
                continue
            if not (example_dir / "meta.json").exists():
                continue
            yield example_dir


def check_output(example_dir: pathlib.Path):
    """
    Returns:
        None          — EXPECTED_OUTPUT.md missing (WARNING, not ERROR)
        "ok"          — EXPECTED_OUTPUT.md exists and has content
        "empty"       — EXPECTED_OUTPUT.md exists but is empty
        "whitespace"  — EXPECTED_OUTPUT.md has only whitespace
    """
    out_path = example_dir / "EXPECTED_OUTPUT.md"
    if not out_path.exists():
        return None

    content = out_path.read_text(encoding="utf-8")
    if len(content) == 0:
        return "empty"
    if not content.strip():
        return "whitespace"
    return "ok"


def main():
    errors = []
    warnings = []
    total = 0

    for example_dir in iter_example_dirs(REPO_ROOT):
        total += 1
        rel = str(example_dir.relative_to(REPO_ROOT))
        result = check_output(example_dir)

        if result is None:
            warnings.append(f"WARNING  {rel}/EXPECTED_OUTPUT.md — missing (run audit.py for full report)")
        elif result == "empty":
            errors.append(f"ERROR    {rel}/EXPECTED_OUTPUT.md — file is empty (0 bytes)")
        elif result == "whitespace":
            errors.append(f"ERROR    {rel}/EXPECTED_OUTPUT.md — file contains only whitespace")

    if warnings:
        for w in warnings:
            print(w)
        print()

    if errors:
        for e in errors:
            print(e)
        print()
        print(f"VALIDATE_OUTPUTS FAILED: {len(errors)} empty EXPECTED_OUTPUT.md file(s) out of {total} examples.")
        sys.exit(1)
    else:
        print(f"VALIDATE_OUTPUTS PASSED: all {total} EXPECTED_OUTPUT.md files are non-empty.")
        sys.exit(0)


if __name__ == "__main__":
    main()
