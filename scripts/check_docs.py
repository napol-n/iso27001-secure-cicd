"""Check local inline Markdown links, fragments, and balanced fenced blocks.

External availability is reviewed separately; no network access is needed in CI.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "node_modules", "reports"}


def prose(path: Path) -> str:
    lines = []
    fence = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    if fence:
        raise ValueError("unclosed fenced code block")
    return "\n".join(lines)


def anchors(content: str) -> set[str]:
    result = set()
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.MULTILINE):
        base = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(base, 0)
        result.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return result


def main() -> int:
    errors = []
    checked = 0
    docs = [p for p in ROOT.rglob("*.md") if not EXCLUDED.intersection(p.relative_to(ROOT).parts)]
    for doc in sorted(docs):
        try:
            content = prose(doc)
        except ValueError as exc:
            errors.append(f"{doc.relative_to(ROOT)}: {exc}")
            continue
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", content):
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc:
                continue
            checked += 1
            path = (doc.parent / unquote(url.path)).resolve() if url.path else doc
            if not path.is_relative_to(ROOT) or not path.exists():
                errors.append(f"{doc.relative_to(ROOT)}: missing or outside repository: {target}")
            elif url.fragment and path.suffix == ".md":
                if unquote(url.fragment) not in anchors(prose(path)):
                    errors.append(f"{doc.relative_to(ROOT)}: missing fragment: {target}")
    for error in errors:
        print(error)
    print(f"Checked {len(docs)} Markdown files and {checked} local links; errors: {len(errors)}")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
