"""Synthetic inputs are assembled in temporary directories; no usable credentials."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from security import secret_scan as scanner

ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "security" / "secret_scan.py"
SYNTHETIC = "synthetic-not-a-real-credential-123"


def assignment(key="API_KEY", value=SYNTHETIC):
    return f'{key} = "{value}"\n'


def write(tmp_path, content, name="source.py"):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def cli(target, cwd=None, entry=SCANNER):
    return subprocess.run(
        [sys.executable, str(entry), str(target)], cwd=cwd,
        capture_output=True, text=True, check=False,
    )


@pytest.mark.parametrize("content", [
    'print("Hello, NovaTech")\n',
    'import os\nAPI_KEY = os.environ["API_KEY"]\n',
    'import os\nPASSWORD = os.getenv("DB_PASSWORD")\n',
    'token_count = 12\nsecret_name = "vault/path"\n',
    assignment(value="${SERVICE_KEY}"),
    assignment(value="YOUR_API_KEY_HERE"),
    assignment(value="EXAMPLE_ONLY_VALUE"),
    assignment(value=""),
], ids=["plain-code", "environment", "getenv", "unrelated-name", "env-template", "your-template", "example-template", "empty"])
def test_clean_and_false_positive_cases(tmp_path, content):
    assert scanner.inspect_file(write(tmp_path, content)) == []


@pytest.mark.parametrize("key,kind", [
    ("API_KEY", "API Key"), ("apiKey", "API Key"), ("PASSWORD", "Password"),
    ("SECRET", "Secret"), ("TOKEN", "Token"), ("db_password", "Password"),
    ("client_secret", "Secret"), ("aws_access_key", "API Key"),
    ("access_token", "Token"), ("passwd", "Password"),
])
def test_original_and_extended_assignments(tmp_path, key, kind):
    assert scanner.inspect_file(write(tmp_path, assignment(key))) == [scanner.Finding(1, kind)]


@pytest.mark.parametrize("value", ["password", "test", "example", "changeme", "123"])
def test_weak_passwords_are_not_allowlisted(tmp_path, value):
    assert scanner.scan_file(write(tmp_path, assignment("PASSWORD", value))) == ["Password"]


@pytest.mark.parametrize("name,content", [
    ("config.json", '{"api_key": "' + SYNTHETIC + '"}'),
    ("config.yaml", 'password: ' + SYNTHETIC),
    (".env", 'export TOKEN=' + SYNTHETIC),
    ("settings.toml", 'client_secret = "' + SYNTHETIC + '"'),
    ("script.js", 'const API_KEY = "' + SYNTHETIC + '";'),
    ("typed.py", 'API_KEY: str = "' + SYNTHETIC + '"'),
    ("no_extension", assignment()),
    ("utf8.py", '\ufeff# สวัสดี\r\n' + assignment()),
], ids=["json", "yaml", "dotenv", "toml", "javascript", "typed-python", "extensionless", "bom-crlf"])
def test_file_formats(tmp_path, name, content):
    assert len(scanner.inspect_file(write(tmp_path, content, name))) == 1


@pytest.mark.parametrize("content,kind", [
    ("AK" + "IA" + "Z" * 16, "AWS Access Key ID"),
    ("gh" + "p_" + "z" * 36, "GitHub Token"),
    ("github_" + "pat_" + "z" * 82, "GitHub Token"),
    ("-----BEGIN " + "PRIVATE KEY-----", "Private Key"),
    ("-----BEGIN RSA " + "PRIVATE KEY-----", "Private Key"),
], ids=["aws-shape", "github-classic", "github-fine-grained", "private-key-header", "rsa-header"])
def test_provider_patterns(tmp_path, content, kind):
    assert scanner.inspect_file(write(tmp_path, content)) == [scanner.Finding(1, kind)]


def test_multiple_findings_and_legacy_api(tmp_path):
    path = write(tmp_path, assignment() + assignment() + assignment("PASSWORD"))
    assert scanner.inspect_file(path) == [
        scanner.Finding(1, "API Key"), scanner.Finding(2, "API Key"), scanner.Finding(3, "Password"),
    ]
    assert scanner.scan_file(path) == ["API Key", "Password"]
    write(tmp_path, assignment("TOKEN"), "nested/config.py")
    result = scanner.scan_path(tmp_path)
    assert len(result.findings) == 4
    assert result.scanned == 2


@pytest.mark.parametrize("dirname", sorted(scanner.EXCLUDED_DIRS))
def test_irrelevant_directories(tmp_path, dirname):
    write(tmp_path, assignment(), dirname + "/ignored.py")
    write(tmp_path, "print(1)")
    result = scanner.scan_path(tmp_path)
    assert not result.findings and not result.errors
    assert result.scanned == 1 and result.skipped == 1


def test_binary_exclusion(tmp_path):
    (tmp_path / "screenshot.PNG").write_bytes(b"\x89PNG\x00\xff")
    write(tmp_path, "print(1)")
    result = scanner.scan_path(tmp_path)
    assert result.skipped == 1 and not result.errors


@pytest.mark.parametrize(
    "content", [b"\xff", b"code\x00data", b"x" * (scanner.MAX_FILE_BYTES + 1)],
    ids=["invalid-utf8", "nul-content", "oversized"],
)
def test_unsupported_text_fails_closed(tmp_path, content):
    path = tmp_path / "bad.py"
    path.write_bytes(content)
    assert scanner.main([str(tmp_path)]) == 2
    with pytest.raises(scanner.ScanError):
        scanner.scan_file(path)


def test_file_size_boundary(tmp_path):
    path = tmp_path / "large.txt"
    path.write_bytes(b"x" * scanner.MAX_FILE_BYTES)
    assert scanner.inspect_file(path) == []


def test_missing_and_empty_targets(tmp_path):
    assert cli(tmp_path / "missing").returncode == 2
    assert cli(tmp_path).returncode == 2


@pytest.mark.parametrize("kind", ["file", "directory", "broken"])
def test_symlinks_not_followed(tmp_path, kind):
    outside = tmp_path / "outside"
    outside.mkdir()
    source = write(outside, assignment())
    target = tmp_path / "target"
    target.mkdir()
    link = target / "link"
    link.symlink_to(outside if kind == "directory" else source if kind == "file" else tmp_path / "missing")
    assert scanner.main([str(target)]) == 2
    assert scanner.main([str(link)]) == 2


def test_unreadable_file(tmp_path, monkeypatch, capsys):
    path = write(tmp_path, "print(1)")

    def denied(*args, **kwargs):
        raise PermissionError("sensitive error payload")

    monkeypatch.setattr(Path, "open", denied)
    assert scanner.main([str(path)]) == 2
    output = capsys.readouterr()
    assert "sensitive error payload" not in output.err
    assert "could not be read" in output.err


def test_unreadable_directory(tmp_path, monkeypatch):
    def denied_walk(target, onerror, **kwargs):
        onerror(PermissionError(13, "denied", str(target)))
        return iter(())

    monkeypatch.setattr(os, "walk", denied_walk)
    assert scanner.main([str(tmp_path)]) == 2


def test_special_file_not_opened(tmp_path):
    path = tmp_path / "pipe"
    os.mkfifo(path)
    assert scanner.main([str(tmp_path)]) == 2


def test_cli_exit_codes_and_redaction(tmp_path):
    path = write(tmp_path, "print(1)")
    clean = cli(path)
    assert clean.returncode == 0 and "Security Gate: PASSED" in clean.stdout
    path.write_text(assignment(), encoding="utf-8")
    failed = cli(path)
    assert failed.returncode == 1 and "Security Gate: FAILED" in failed.stdout
    assert "[REDACTED]" in failed.stdout and ":1" in failed.stdout
    assert SYNTHETIC not in failed.stdout + failed.stderr
    (tmp_path / "bad.py").write_bytes(b"\xff")
    error = cli(tmp_path)
    assert error.returncode == 2 and "scan incomplete" in error.stdout
    assert SYNTHETIC not in error.stdout + error.stderr


def test_default_target_and_original_entrypoint(tmp_path):
    write(tmp_path, "print(1)", "app/clean.py")
    default = subprocess.run([sys.executable, str(SCANNER)], cwd=tmp_path, capture_output=True, check=False)
    assert default.returncode == 0
    # app/app.py is the original runnable demo and is preserved unchanged.
    assert cli("app", cwd=tmp_path, entry=ROOT / "app" / "app.py").returncode == 0
    write(tmp_path, assignment(), "app/secret.py")
    assert cli("app", cwd=tmp_path, entry=ROOT / "app" / "app.py").returncode == 1
