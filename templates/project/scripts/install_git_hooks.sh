#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

chmod +x scripts/install_git_hooks.sh .githooks/pre-commit .githooks/pre-push
git config core.hooksPath .githooks

printf 'Installed repository git hooks.\n'
printf 'pre-commit will now run scripts/check_large_files.py before every commit.\n'
printf 'pre-push will now run scripts/check.sh when present, otherwise scripts/check_large_files.py.\n'
printf 'This is the no-cost local fallback for private repositories without GitHub required checks.\n'
