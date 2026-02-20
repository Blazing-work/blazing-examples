#!/usr/bin/env bash
# CI entry point: runs all blazing-examples validation scripts.
# Exit code is the number of failures (0 = all passed).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TESTS_DIR="$REPO_ROOT/tests"
FAILURES=0

echo "=== blazing-examples validation ==="

run_check() {
  local name="$1"
  local script="$2"
  echo ""
  echo "--- $name ---"
  if python3 "$TESTS_DIR/$script"; then
    echo "$name: PASSED"
  else
    echo "$name: FAILED"
    FAILURES=$((FAILURES + 1))
  fi
}

run_check "audit"            "audit.py"
run_check "lint_meta"        "lint_meta.py"
run_check "validate_outputs" "validate_outputs.py"

echo ""
echo "=== Results: $FAILURES failure(s) ==="
exit $FAILURES
