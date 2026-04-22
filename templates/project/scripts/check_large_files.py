#!/usr/bin/env python3
"""Fail CI when oversized source files grow or new giant files appear."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CONFIG_PATH = Path(".governance/large_file_policy.json")


@dataclass(frozen=True)
class Finding:
    path: str
    line_count: int
    limit: int
    kind: str
    message: str


def load_policy(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"large-file policy not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"large-file policy is not valid JSON: {path}: {exc}") from exc


def tracked_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [
        item
        for item in result.stdout.decode("utf-8", errors="replace").split("\0")
        if item
    ]


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return sum(1 for _ in handle)


def legacy_limit(entry: Any) -> int:
    if isinstance(entry, dict):
        return int(entry.get("max_lines") or 0)
    return int(entry or 0)


def is_excluded(rel_path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch(rel_path, pattern) for pattern in patterns)


def should_check(rel_path: str, policy: dict[str, Any]) -> bool:
    if is_excluded(rel_path, policy.get("exclude_globs") or []):
        return False
    extensions = {str(item).lower() for item in policy.get("source_extensions") or []}
    return Path(rel_path).suffix.lower() in extensions


def evaluate(repo_root: Path, policy: dict[str, Any]) -> dict[str, Any]:
    max_lines = int(policy.get("max_lines") or 800)
    legacy_files = policy.get("legacy_files") or {}
    findings: list[Finding] = []
    checked_files = 0
    oversized_files = 0

    for rel_path in tracked_files(repo_root):
        if not should_check(rel_path, policy):
            continue
        full_path = repo_root / rel_path
        if not full_path.is_file():
            continue

        checked_files += 1
        count = line_count(full_path)
        legacy_entry = legacy_files.get(rel_path)
        if legacy_entry is not None:
            baseline = legacy_limit(legacy_entry)
            if count > baseline:
                findings.append(
                    Finding(
                        path=rel_path,
                        line_count=count,
                        limit=baseline,
                        kind="legacy_growth",
                        message=(
                            f"{rel_path} has {count} lines, above its frozen "
                            f"legacy baseline of {baseline}. Split code out or "
                            "update the baseline with an explicit exception."
                        ),
                    )
                )
            if count > max_lines:
                oversized_files += 1
            continue

        if count > max_lines:
            oversized_files += 1
            findings.append(
                Finding(
                    path=rel_path,
                    line_count=count,
                    limit=max_lines,
                    kind="new_oversized_file",
                    message=(
                        f"{rel_path} has {count} lines, above the hard limit of "
                        f"{max_lines}. Split it before merge or add an explicit "
                        "legacy exception with a freeze baseline."
                    ),
                )
            )

    return {
        "checked_files": checked_files,
        "oversized_files": oversized_files,
        "max_lines": max_lines,
        "findings": [finding.__dict__ for finding in findings],
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "[large-files] checked_files={checked_files} oversized_files={oversized_files} max_lines={max_lines}".format(
            **report
        )
    ]
    findings = report.get("findings") or []
    if not findings:
        lines.append("[large-files] ok")
        return "\n".join(lines)

    lines.append("[large-files] violations:")
    for finding in findings:
        lines.append(f"- {finding['kind']}: {finding['message']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to large-file policy JSON.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    policy = load_policy(args.config)
    report = evaluate(repo_root, policy)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
