"""Prove the configured SAST command accepts clean code and rejects unsafe code."""

import subprocess
import sys

import pytest


@pytest.mark.parametrize("unsafe,expected", [(False, 0), (True, 1)])
def test_bandit_gate(tmp_path, unsafe, expected):
    path = tmp_path / "sample.py"
    source = 'print("NovaTech")\n'
    if unsafe:
        source = 'result = ' + 'eval' + '(input())\n'
    path.write_text(source, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "bandit", str(path), "--ignore-nosec", "--format", "custom",
         "--msg-template", "{relpath}:{line} {test_id} {severity} {confidence}"],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == expected
    if unsafe:
        assert "B307" in result.stdout
        assert source.strip() not in result.stdout + result.stderr
