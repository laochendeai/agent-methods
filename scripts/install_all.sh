#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$SCRIPT_DIR/install_codex_skills.sh"
bash "$SCRIPT_DIR/install_claude_skills.sh"
