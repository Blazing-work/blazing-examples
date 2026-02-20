"""
audit.py — Per-example directory completeness audit.

Checks that every example directory contains the three required files:
  flow.py, meta.json, EXPECTED_OUTPUT.md

Usage (from blazing-examples root):
    python3 tests/audit.py

Exit codes:
    0 — all examples have all required files
    1 — one or more examples are missing required files
"""

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent
REQUIRED_FILES = ["flow.py", "meta.json", "EXPECTED_OUTPUT.md"]


def iter_example_dirs(repo_root: pathlib.Path):
    """Yield all example directories (category/example pairs)."""
    for cat_dir in sorted(repo_root.glob("[0-9][0-9]_*/")):
        if not cat_dir.is_dir():
            continue
        for example_dir in sorted(cat_dir.iterdir()):
            if not example_dir.is_dir():
                continue
            if example_dir.name == "__pycache__":
                continue
            # Only treat as example if meta.json is present
            if not (example_dir / "meta.json").exists():
                continue
            yield example_dir


def audit(repo_root: pathlib.Path):
    """Run audit and return list of (example_path, missing_files) tuples."""
    results = []
    for example_dir in iter_example_dirs(repo_root):
        missing = [f for f in REQUIRED_FILES if not (example_dir / f).exists()]
        results.append((example_dir, missing))
    return results


def main():
    results = audit(REPO_ROOT)

    total = len(results)
    failures = [(path, missing) for path, missing in results if missing]

    # Print header
    col_w = max((len(str(p.relative_to(REPO_ROOT))) for p, _ in results), default=40)
    header = f"{'EXAMPLE':<{col_w}}  flow.py    meta.json  EXPECTED_OUTPUT.md"
    print(header)
    print("-" * len(header))

    for example_dir, missing in results:
        rel = str(example_dir.relative_to(REPO_ROOT))
        flow_ok = "OK      " if "flow.py" not in missing else "MISSING "
        meta_ok = "OK       " if "meta.json" not in missing else "MISSING  "
        out_ok = "OK" if "EXPECTED_OUTPUT.md" not in missing else "MISSING"
        print(f"{rel:<{col_w}}  {flow_ok}   {meta_ok}  {out_ok}")

    print()
    if failures:
        print(f"AUDIT FAILED: {len(failures)}/{total} examples have missing files.")
        for path, missing in failures:
            rel = str(path.relative_to(REPO_ROOT))
            print(f"  {rel}: missing {', '.join(missing)}")
        sys.exit(1)
    else:
        print(f"AUDIT PASSED: all {total} examples have all required files.")
        sys.exit(0)


if __name__ == "__main__":
    main()
