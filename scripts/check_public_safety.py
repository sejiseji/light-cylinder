from __future__ import annotations

import argparse
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".pyright",
    "build",
    "dist",
    "htmlcov",
    "logs",
    "captures",
    "screenshots",
}

TEXT_SUFFIXES = {
    ".cfg",
    ".css",
    ".csv",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("macos_home_path", re.compile(r"/Users/[A-Za-z0-9._-]+(?:/|$)")),
    ("linux_home_path", re.compile(r"/home/[A-Za-z0-9._-]+(?:/|$)")),
    ("windows_home_path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+(?:\\|$)")),
    ("private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b")),
    (
        "api_key",
        re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{20,}"),
    ),
    (
        "private_ip",
        re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b"),
    ),
    ("email_review", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("local_share_path", re.compile(r"(?i)\b(?:smb|afp|file)://[^\s]+")),
    ("tailscale_hostname", re.compile(r"\b[A-Za-z0-9-]+\.ts\.net\b")),
]


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    category: str
    preview: str


@dataclass(frozen=True)
class ScanResult:
    scanned_files: int
    skipped_binary_files: int
    findings: tuple[Finding, ...]


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS or part.endswith(".egg-info") for part in path.parts)


def is_probably_text(path: Path) -> bool:
    if path.name in {".gitignore"}:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def git_tracked_files(root: Path) -> list[Path]:
    try:
        completed = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [root / line for line in completed.stdout.splitlines() if line.strip()]


def candidate_files(root: Path) -> list[Path]:
    tracked = set(git_tracked_files(root))
    candidates: set[Path] = set()

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if is_excluded(relative):
            continue
        if is_probably_text(path):
            candidates.add(path)

    return sorted(tracked | candidates)


def mask_value(value: str) -> str:
    collapsed = value.replace("\\", "/")
    if len(collapsed) <= 10:
        return "<masked>"
    return f"{collapsed[:4]}...{collapsed[-4:]}"


def scan_file(root: Path, path: Path) -> tuple[list[Finding], bool]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [], True

    findings: list[Finding] = []
    relative = path.relative_to(root)
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                findings.append(
                    Finding(
                        path=relative,
                        line_number=line_number,
                        category=category,
                        preview=mask_value(match.group(0)),
                    )
                )
    return findings, False


def scan_repository(root: Path) -> ScanResult:
    scanned_files = 0
    skipped_binary_files = 0
    findings: list[Finding] = []

    for path in candidate_files(root):
        if not path.exists() or is_excluded(path.relative_to(root)):
            continue
        file_findings, skipped_binary = scan_file(root, path)
        if skipped_binary:
            skipped_binary_files += 1
            continue
        scanned_files += 1
        findings.extend(file_findings)

    return ScanResult(
        scanned_files=scanned_files,
        skipped_binary_files=skipped_binary_files,
        findings=tuple(findings),
    )


def print_result(result: ScanResult) -> None:
    counts = Counter(finding.category for finding in result.findings)
    print(f"scanned files: {result.scanned_files}")
    print(f"skipped binary files: {result.skipped_binary_files}")
    print(f"findings count: {len(result.findings)}")

    if counts:
        print("findings by category:")
        for category, count in sorted(counts.items()):
            print(f"- {category}: {count}")
        print("findings:")
        for finding in result.findings:
            print(f"- {finding.path}:{finding.line_number}: {finding.category}: {finding.preview}")

    print("FAIL" if result.findings else "PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    result = scan_repository(args.root.resolve())
    print_result(result)
    return 1 if result.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
