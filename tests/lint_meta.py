"""
lint_meta.py — meta.json schema and quality validation.

Validates every example's meta.json for:
  - All required fields present
  - description length >= 80 characters
  - tags is a non-empty list
  - difficulty is one of: Beginner, Intermediate, Advanced
  - products is a non-empty list

Usage (from blazing-examples root):
    python3 tests/lint_meta.py

Exit codes:
    0 — all meta.json files pass validation
    1 — one or more violations found
"""

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent

REQUIRED_FIELDS = [
    "id",
    "title",
    "description",
    "tags",
    "category",
    "difficulty",
    "time",
    "products",
    "primaryProduct",
]

VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}
DESCRIPTION_MIN_LEN = 80


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
            meta_path = example_dir / "meta.json"
            if not meta_path.exists():
                continue
            yield example_dir, meta_path


def lint_meta(meta_path: pathlib.Path):
    """Return list of violation strings for a single meta.json."""
    violations = []

    try:
        with meta_path.open() as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            violations.append(f"missing required field: '{field}'")

    # description length
    desc = data.get("description", "")
    if isinstance(desc, str):
        if len(desc) < DESCRIPTION_MIN_LEN:
            violations.append(
                f"description too short: {len(desc)} chars (minimum {DESCRIPTION_MIN_LEN})"
            )
    elif "description" in data:
        violations.append("description must be a string")

    # tags non-empty list
    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            violations.append("tags must be a list")
        elif len(tags) == 0:
            violations.append("tags must be non-empty")

    # difficulty value
    difficulty = data.get("difficulty")
    if difficulty is not None:
        if difficulty not in VALID_DIFFICULTIES:
            violations.append(
                f"difficulty '{difficulty}' not in {sorted(VALID_DIFFICULTIES)}"
            )

    # products non-empty list
    products = data.get("products")
    if products is not None:
        if not isinstance(products, list):
            violations.append("products must be a list")
        elif len(products) == 0:
            violations.append("products must be non-empty")

    return violations


def main():
    all_violations = []

    for example_dir, meta_path in iter_example_dirs(REPO_ROOT):
        rel = str(meta_path.relative_to(REPO_ROOT))
        violations = lint_meta(meta_path)
        if violations:
            all_violations.append((rel, violations))

    total_examples = sum(1 for _ in iter_example_dirs(REPO_ROOT))

    if all_violations:
        print(f"LINT FAILED: {len(all_violations)}/{total_examples} examples have meta.json violations.\n")
        for rel, violations in all_violations:
            print(f"  {rel}:")
            for v in violations:
                print(f"    - {v}")
        sys.exit(1)
    else:
        print(f"LINT PASSED: all {total_examples} meta.json files are valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
