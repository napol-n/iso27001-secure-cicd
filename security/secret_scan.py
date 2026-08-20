import re
import sys
from pathlib import Path


TARGET_DIRECTORY = Path("app")


SECRET_PATTERNS = {
    "API Key": re.compile(
        r'API_KEY\s*=\s*["\'][^"\']+["\']',
        re.IGNORECASE
    ),
    "Password": re.compile(
        r'PASSWORD\s*=\s*["\'][^"\']+["\']',
        re.IGNORECASE
    ),
    "Secret": re.compile(
        r'SECRET\s*=\s*["\'][^"\']+["\']',
        re.IGNORECASE
    ),
    "Token": re.compile(
        r'TOKEN\s*=\s*["\'][^"\']+["\']',
        re.IGNORECASE
    ),
}


def scan_file(file_path: Path) -> list[str]:
    findings = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings

    for secret_type, pattern in SECRET_PATTERNS.items():
        if pattern.search(content):
            findings.append(secret_type)

    return findings


def main():
    findings = []

    print("================================")
    print(" NovaTech Secret Security Scan")
    print("================================")
    print()

    for file_path in TARGET_DIRECTORY.rglob("*.py"):
        file_findings = scan_file(file_path)

        for secret_type in file_findings:
            findings.append((file_path, secret_type))

            print(
                f"[HIGH] Potential {secret_type} detected "
                f"in {file_path}"
            )

    print()

    if findings:
        print("Security Gate: FAILED")
        print(f"Total findings: {len(findings)}")
        sys.exit(1)

    print("Security Gate: PASSED")
    print("No hardcoded secrets detected.")
    sys.exit(0)


if __name__ == "__main__":
    main()
    
