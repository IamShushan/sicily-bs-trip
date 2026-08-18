#!/usr/bin/env python3
"""Block sensitive personal data and unsafe binary files from entering Git history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MAX_TEXT_BYTES = 2 * 1024 * 1024
ZERO_SHA = "0" * 40
BLOCKED_EXTENSIONS = {
    ".7z",
    ".doc",
    ".docx",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".numbers",
    ".pages",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".rar",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}


@dataclass(frozen=True)
class Finding:
    category: str
    path: str
    line: int | None = None


def run_git(*args: str, input_text: str | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=None if input_text is None else input_text.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return result.stdout


def luhn_valid(value: str) -> bool:
    digits = [int(char) for char in value]
    parity = len(digits) % 2
    total = 0
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def israeli_id_valid(value: str) -> bool:
    if len(value) != 9 or not value.isdigit():
        return False
    total = 0
    for index, char in enumerate(value):
        digit = int(char) * (1 if index % 2 == 0 else 2)
        total += digit if digit < 10 else digit - 9
    return total % 10 == 0


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def regex_findings(
    text: str, path: str, category: str, pattern: str, flags: int = re.IGNORECASE
) -> list[Finding]:
    return [
        Finding(category, path, line_number(text, match.start()))
        for match in re.finditer(pattern, text, flags)
    ]


def scan_text(text: str, path: str) -> list[Finding]:
    findings: list[Finding] = []

    card_pattern = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
    for match in card_pattern.finditer(text):
        digits = re.sub(r"\D", "", match.group())
        if 13 <= len(digits) <= 19 and luhn_valid(digits):
            findings.append(Finding("payment-card number", path, line_number(text, match.start())))

    id_pattern = re.compile(
        r"(?:תעודת\s*זהות|ת[\"״']?ז|israeli?\s+id|identity\s+(?:number|no\.?))"
        r"\s*[:#-]?\s*([0-9][0-9 -]{7,15}[0-9])",
        re.IGNORECASE,
    )
    for match in id_pattern.finditer(text):
        digits = re.sub(r"\D", "", match.group(1))
        if israeli_id_valid(digits):
            findings.append(Finding("Israeli identity number", path, line_number(text, match.start())))

    passport_pattern = re.compile(
        r"(?:passport|דרכון|passaporto)\s*(?:number|no\.?|מספר)?\s*[:#-]?\s*([A-Z0-9]{6,12})",
        re.IGNORECASE,
    )
    for match in passport_pattern.finditer(text):
        value = match.group(1)
        if any(char.isdigit() for char in value):
            findings.append(Finding("passport number", path, line_number(text, match.start())))

    contextual_patterns = {
        "card security code": r"\b(?:cvv|cvc|security\s+code)\s*[:#-]?\s*\d{3,4}\b",
        "booking reference": (
            r"(?:\bpnr\b|booking\s*(?:reference|ref|code)\b|reservation\s*(?:reference|code)\b|"
            r"מספר\s*הזמנה|קוד\s*הזמנה)\s*[:#-]?\s*[A-Z0-9][A-Z0-9-]{4,13}\b"
        ),
        "electronic ticket number": (
            r"(?:e-?ticket|electronic\s+ticket|כרטיס\s*אלקטרוני)\s*[:#-]?\s*\d{3}[ -]?\d{10}\b"
        ),
        "IBAN": r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
        "private email address": (
            r"\b[A-Z0-9._%+-]+@(?:gmail|googlemail|outlook|hotmail|icloud|yahoo|protonmail|"
            r"proton|walla)\.[A-Z]{2,}\b|"
            r"(?:private|personal|פרטי|אישי)\s+(?:e-?mail|email|אימייל|מייל)\s*[:#-]?\s*"
            r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
        ),
        "private phone number": (
            r"(?:phone|mobile|whatsapp|טלפון|נייד|וואטסאפ)\s*[:#-]?\s*"
            r"(?:\+?\d[\d ()-]{7,}\d)"
        ),
        "date of birth": (
            r"(?:date\s+of\s+birth|dob|תאריך\s*לידה)\s*[:#-]?\s*"
            r"(?:\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{4}[./-]\d{1,2}[./-]\d{1,2})"
        ),
        "private key": r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----",
        "credential": (
            r"\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)\b"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}"
        ),
    }
    for category, pattern in contextual_patterns.items():
        findings.extend(regex_findings(text, path, category, pattern))

    return list(dict.fromkeys(findings))


def scan_blob(path: str, data: bytes) -> list[Finding]:
    suffix = Path(path).suffix.lower()
    if suffix in BLOCKED_EXTENSIONS:
        return [Finding(f"blocked file type ({suffix})", path)]
    if len(data) > MAX_TEXT_BYTES:
        return [Finding("file exceeds the privacy scan size limit", path)]
    if b"\0" in data:
        return [Finding("binary file", path)]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [Finding("non-UTF-8 or binary file", path)]
    return scan_text(text, path)


def nul_items(data: bytes) -> list[str]:
    return [item.decode("utf-8", errors="surrogateescape") for item in data.split(b"\0") if item]


def changed_paths_for_commit(commit: str) -> list[str]:
    return nul_items(
        run_git(
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "--diff-filter=ACMR",
            "-r",
            "-z",
            commit,
        )
    )


def scan_commits(commits: Iterable[str]) -> list[Finding]:
    findings: list[Finding] = []
    for commit in commits:
        for path in changed_paths_for_commit(commit):
            findings.extend(scan_blob(path, run_git("show", f"{commit}:{path}")))
    return list(dict.fromkeys(findings))


def scan_staged() -> list[Finding]:
    paths = nul_items(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"))
    findings: list[Finding] = []
    for path in paths:
        findings.extend(scan_blob(path, run_git("show", f":{path}")))
    return list(dict.fromkeys(findings))


def scan_all_files() -> list[Finding]:
    findings: list[Finding] = []
    for path in nul_items(run_git("ls-files", "-z")):
        findings.extend(scan_blob(path, (ROOT / path).read_bytes()))
    return list(dict.fromkeys(findings))


def commits_for_range(revision_range: str) -> list[str]:
    return run_git("rev-list", "--reverse", revision_range).decode().splitlines()


def commits_from_pre_push(remote: str, lines: Iterable[str]) -> list[str]:
    commits: set[str] = set()
    for raw_line in lines:
        parts = raw_line.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if local_sha == ZERO_SHA:
            continue
        if remote_sha == ZERO_SHA:
            output = run_git("rev-list", local_sha, "--not", f"--remotes={remote}")
        else:
            output = run_git("rev-list", f"{remote_sha}..{local_sha}")
        commits.update(output.decode().splitlines())
    return sorted(commits)


def print_findings(findings: list[Finding]) -> None:
    print("Privacy scan blocked this operation. Sensitive values are masked.", file=sys.stderr)
    for finding in findings:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        print(f"- {location}: {finding.category} detected ([REDACTED])", file=sys.stderr)
    print("Remove the private data; do not add it to an allowlist.", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true", help="scan staged files")
    mode.add_argument("--range", dest="revision_range", help="scan every commit in a Git range")
    mode.add_argument("--pre-push", metavar="REMOTE", help="scan commits described on stdin by Git")
    mode.add_argument("--all-files", action="store_true", help="scan all tracked files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.staged:
            findings = scan_staged()
        elif args.revision_range:
            findings = scan_commits(commits_for_range(args.revision_range))
        elif args.pre_push:
            findings = scan_commits(commits_from_pre_push(args.pre_push, sys.stdin))
        else:
            findings = scan_all_files()
    except (OSError, RuntimeError) as error:
        print(f"Privacy scan failed closed: {error}", file=sys.stderr)
        return 2

    if findings:
        print_findings(findings)
        return 1
    print("Privacy scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
