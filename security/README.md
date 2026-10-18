# Secret detection design and operating procedure

The authoritative CI entry point is [secret_scan.py](secret_scan.py). The original
[app demo](../app/app.py) remains unchanged for regression comparison; it is not a
web server and does not inherit the new scanner's coverage. Use the security script
for control operation.

## Contract

Run from the repository root with Python 3.12 or later:

```sh
python security/secret_scan.py       # original default target: app/
python security/secret_scan.py .     # CI scope: current working tree
python security/secret_scan.py path/to/file
```

| Exit | Meaning | Required response |
|---|---|---|
| 0 | Eligible files inspected; no configured pattern matched | Continue with the other gates; this is not proof of absence of secrets |
| 1 | One or more potential secrets | Review locally; remove the secret, revoke/rotate it if real, and rerun |
| 2 | Missing/empty target, unreadable content, unsupported input, or CLI error | Repair the scan coverage; do not treat this as clean |

The scanner reports category, escaped path, line number, counts, and status. It
never reports the matched value or source line. Multiple occurrences are reported;
a provider token assigned to a sensitive name can match two categories. Counts are
rule matches, not a count of unique credentials. The compatibility function
`scan_file(Path)` still returns unique category names, but unreadable text now raises
`ScanError` instead of silently returning no findings.

## Coverage and exclusions

- Quoted assignments to API key, password/passwd, secret, token, access key,
  secret key, and client secret names, including underscore prefixes and `str` annotations.
- Quoted JSON-style keys; unquoted assignments in `.env*`, YAML, TOML, INI, CFG,
  and properties files; selected AWS/GitHub token shapes and private-key headers.
- All eligible UTF-8 text, including extensionless files, dotfiles, tests, docs,
  and workflow configuration. UTF-8 BOM and CRLF input are accepted.
- Excluded directory names: `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`,
  `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.tox`, `build`, `dist`, `reports`.
  These are excluded wherever they occur. `.gitignore` is deliberately not used:
  an accidentally present `.env` must still be inspected locally.
- Known binary suffixes and `.DS_Store` are excluded; the exact suffix set is in
  the script. Other non-UTF-8 or NUL-containing files fail the scan.
- Eligible files over 1 MiB, symlinks outside excluded directories, special files,
  and read/traversal errors fail with exit 2. Symlinks are not followed. Empty or
  entirely excluded targets also fail. Run in a stable checkout; filesystem races
  against a concurrent malicious writer are outside this lab's threat model.

## False positives and false negatives

Only explicit `${NAME}`, `YOUR_*_HERE`, and `EXAMPLE_ONLY_*` placeholders are
ignored in generic assignment rules. Provider patterns are still checked. Empty
strings and runtime environment lookups do not match the generic quoted rule.
Weak values such as “password”, “test”, or “changeme” are not blanket exemptions.
Comments and documentation containing secret-shaped text can produce findings;
review them as potential exposure rather than automatically suppressing comments.

This is pattern matching, not data-flow analysis or credential validation. It can
miss multiline/concatenated/encoded values, uncommon names and providers, alternate
encodings, templating syntax, nested YAML structures, or secrets in excluded files
and Git history. Binary suffixes can hide text and exclusions can be abused. Short
noncredential strings assigned to a sensitive name may be false positives. A
placeholder-shaped real credential would be missed. No result establishes that a
credential is valid, invalid, revoked, or absent from earlier commits.

Tests construct clearly synthetic values in temporary directories. Never add a
real credential to a test or an issue. For a real exposure, revoke/rotate first,
review access logs, then remove the value and assess history cleanup.

## Established scanner decision

[Gitleaks](https://github.com/gitleaks/gitleaks) was reviewed as a complementary
scanner for broader provider rules and Git history. It is deferred from this
small teaching pipeline to keep the original Python control understandable and
avoid introducing a binary distribution/update process in the same change.
This is a conscious coverage limitation, not equivalence to a production scanner.
Before production use, evaluate a maintained secret scanner with a pinned release,
redacted output, history coverage, narrowly reviewed exceptions, and pre-commit or
push protection. Do not merely ignore historical findings to obtain a green run.

[Bandit](https://bandit.readthedocs.io/en/latest/man/bandit.html) complements the
custom check with Python SAST. CI uses custom metadata-only output and does not
honor `nosec` suppressions. [pip-audit](https://github.com/pypa/pip-audit) checks the
installed tool environment and transitive packages against known advisories; it
does not establish that a package is trustworthy or free of unknown vulnerabilities.
