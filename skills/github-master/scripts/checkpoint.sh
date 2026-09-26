#!/usr/bin/env bash
# checkpoint.sh — stage and commit all current local changes as a safety-net checkpoint.
# Local only: never pushes. Skips silently (no empty commit) if the working tree is clean.
# Usage: ./checkpoint.sh ["optional short note"]

set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository." >&2
  exit 1
fi

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing to checkpoint — working tree is clean."
  exit 0
fi

note="${1:-}"
timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

if [ -n "$note" ]; then
  message="checkpoint: ${note} (${timestamp})"
else
  message="checkpoint: ${timestamp}"
fi

git add -A
git commit -m "$message" --quiet
echo "Checkpoint committed: $message"
