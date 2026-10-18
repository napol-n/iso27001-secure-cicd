"""Small, deliberately conservative secret gate. See security/README.md."""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TARGET_DIRECTORY = Path("app")
MAX_FILE_BYTES = 1_048_576
EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", "build", "dist", "reports",
}
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz",
    ".woff", ".woff2", ".pyc", ".pyo", ".mp4", ".sqlite", ".db",
}
CONFIG_SUFFIXES = {".yaml", ".yml", ".toml", ".ini", ".cfg", ".properties"}
KEY = r"(?P<key>(?:[a-z][a-z0-9]*_)*(?:api_?key|password|passwd|secret|token|access_key|secret_key|client_secret))"
ASSIGNMENT = re.compile(
    r"(?<![\w])['\"]?" + KEY + r"['\"]?(?:\s*:\s*str)?\s*[:=]\s*"
    r"(?P<quote>['\"])(?P<value>[^'\"\r\n]+)(?P=quote)", re.IGNORECASE,
)
UNQUOTED = re.compile(
    r"^\s*(?:export\s+)?" + KEY + r"\s*[:=]\s*(?P<value>[^\s'\"#]+)",
    re.IGNORECASE | re.MULTILINE,
)
SECRET_PATTERNS = {
    "AWS Access Key ID": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GitHub Token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{82}\b"),
    "Private Key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
}


@dataclass(frozen=True)
class Finding:
    line: int
    kind: str


@dataclass
class ScanResult:
    findings: list[tuple[Path, Finding]] = field(default_factory=list)
    errors: list[tuple[Path, str]] = field(default_factory=list)
    scanned: int = 0
    skipped: int = 0


class ScanError(Exception):
    """A file could not be safely inspected; never contains source content."""


def is_placeholder(value: str) -> bool:
    """Only explicit template markers; weak passwords are still findings."""
    return bool(re.fullmatch(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|YOUR_[A-Z0-9_]+_HERE|EXAMPLE_ONLY_[A-Z0-9_]+", value))


def secret_kind(key: str) -> str:
    key = key.lower()
    if "password" in key or "passwd" in key:
        return "Password"
    if "token" in key:
        return "Token"
    if "key" in key:
        return "API Key"
    return "Secret"


def inspect_file(file_path: Path) -> list[Finding]:
    """Inspect a regular UTF-8 file with a bounded read, without retaining values."""
    try:
        if file_path.is_symlink() or not file_path.is_file():
            raise ScanError("not a regular file (symlinks are not followed)")
        with file_path.open("rb") as source:
            raw = source.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            raise ScanError("file exceeds 1 MiB scan limit")
        if b"\x00" in raw:
            raise ScanError("unexpected binary or UTF-16 content")
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ScanError("file is not UTF-8 text") from exc
    except OSError as exc:
        raise ScanError("file could not be read") from exc

    matches = []
    patterns = [ASSIGNMENT]
    if file_path.suffix.lower() in CONFIG_SUFFIXES or file_path.name.startswith(".env"):
        patterns.append(UNQUOTED)
    for pattern in patterns:
        for match in pattern.finditer(content):
            if not is_placeholder(match["value"]):
                matches.append((match.start(), secret_kind(match["key"])))
    for kind, pattern in SECRET_PATTERNS.items():
        matches.extend((match.start(), kind) for match in pattern.finditer(content))
    return [Finding(content.count("\n", 0, offset) + 1, kind) for offset, kind in sorted(set(matches))]


def scan_file(file_path: Path) -> list[str]:
    """Compatibility API: unique categories, as in the original scanner.

    Unreadable or unsupported text now raises ScanError instead of passing silently.
    """
    return list(dict.fromkeys(finding.kind for finding in inspect_file(file_path)))


def scan_path(target: Path) -> ScanResult:
    result = ScanResult()

    def visit(path: Path) -> None:
        if path.is_symlink():
            result.errors.append((path, "symlink is not followed"))
        elif path.suffix.lower() in BINARY_SUFFIXES or path.name == ".DS_Store":
            result.skipped += 1
        else:
            try:
                result.findings.extend((path, finding) for finding in inspect_file(path))
                result.scanned += 1
            except ScanError as exc:
                result.errors.append((path, str(exc)))

    if target.is_symlink() or not target.exists():
        result.errors.append((target, "target missing or a symlink"))
    elif target.is_dir():
        def walk_error(error: OSError) -> None:
            result.errors.append((Path(error.filename or target), "directory could not be read"))

        for directory, dirs, files in os.walk(target, onerror=walk_error, followlinks=False):
            for name in sorted(dirs[:]):
                path = Path(directory) / name
                if name in EXCLUDED_DIRS:
                    dirs.remove(name)
                    result.skipped += 1
                elif path.is_symlink():
                    dirs.remove(name)
                    result.errors.append((path, "symlink directory is not followed"))
            dirs.sort()
            for name in sorted(files):
                visit(Path(directory) / name)
    else:
        visit(target)
    if result.scanned == 0 and not result.errors:
        result.errors.append((target, "no eligible text files scanned"))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, default=TARGET_DIRECTORY)
    args = parser.parse_args(argv)
    print("NovaTech Secret Security Scan")
    result = scan_path(args.target)
    for path, finding in result.findings:
        print(f"[HIGH] Potential {finding.kind} in {str(path)!r}:{finding.line} [REDACTED]")
    for path, reason in result.errors:
        print(f"[ERROR] {str(path)!r}: {reason}", file=sys.stderr)
    print(f"Scanned: {result.scanned}; excluded entries: {result.skipped}; findings: {len(result.findings)}; errors: {len(result.errors)}")
    if result.errors:
        print("Security Gate: ERROR (scan incomplete)")
        return 2
    if result.findings:
        print("Security Gate: FAILED")
        return 1
    print("Security Gate: PASSED")
    print("No hardcoded secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
