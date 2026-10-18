# Validation and Portfolio Review Report

## Context and provenance

Review date: 2026-10-18 (Asia/Bangkok). Repository baseline:
`ea88e2e558cc9d8ac51d348b428448f46a460a02`. Dedicated branch:
`audit/secure-cicd-portfolio`. Local execution: macOS arm64, Python 3.13.5,
isolated virtual environment. CI is configured for Ubuntu 24.04/Python 3.12.

Actual machine-readable results and source hashes are in
[local-validation.json](local-validation.json); individual assertions are in
[pytest.xml](pytest.xml). A command's expected result is recorded separately from
its observed exit/output. This is a maintainer-performed assessment, not an
independent audit. No real credentials were required or committed.

## Findings and disposition

| Review finding | Change / disposition |
|---|---|
| Minimal README; unclear distinction between scenario and implementation | Professional overview, architecture, execution instructions, traceability, evidence, and limitations |
| Incomplete fenced block; failed screenshot overstated detection evidence | Repaired Markdown; preserved both images; historical failure marked inconclusive for detection |
| Scanner only inspected Python and silently skipped invalid text | Broader text/configuration patterns, redaction, bounded reads, explicit exclusions, exit 2 for incomplete scans |
| No automated regression tests | 65 tests covering clean/negative cases, edge handling, CLI exits, original demo, and Bandit rejection |
| Only custom scanning in CI; mutable action tags and implicit token permissions | Tests, Bandit, pip-audit, link check, immutable Actions, read-only permissions, disabled credential persistence, timeout, retained JUnit |
| Original residual High risk could be mistaken for accepted risk | Retained IDs/scores; clarified provisional estimates, ownership, open treatment, and lack of acceptance |
| No coverage for dependency/code flaws or gate bypass in risk records | Added RISK-002/003 and CTRL-002/003/004; added effectiveness assessment and A.8.8 mapping |
| Bundled pip 25.1.1 had reported advisories | Pinned pip 26.2.1 and reran installed-environment audit; no advisory suppression |
| Default pytest case names exported synthetic token shapes and a large fixture into XML | Added descriptive case IDs; final evidence is compact and passes the same secret gate without adding exclusions |
| Merge enforcement missing | Open risk; no repository settings changed and no blocked-merge claim |

## Validation status

| Check | Expected | Observed / evidence |
|---|---|---|
| pytest | All regression and negative-gate assertions pass | 65 passed locally; [XML](pytest.xml) |
| Original app and default scanner | Exit 0 on clean application | Passed; app source unchanged from baseline |
| Current-tree custom secret scan | Exit 0 with no findings/errors | Passed on reviewed working tree; excluded scope documented |
| Synthetic secret and incomplete scan | Exits 1 and 2 respectively | Passed rejection assertions; no matched value in output |
| Bandit scoped source | Exit 0 | Passed; metadata-only output |
| Bandit negative example | Exit 1 with B307 | Passed rejection assertion |
| Dependency audit after remediation | Exit 0, no known advisories | 34 installed packages, zero reported vulnerabilities; actual JSON and captured exit in linked evidence |
| Dependency negative probe | Nonzero for known-vulnerable requirement | Exit 1; urllib3 1.26.5 was not installed |
| GitHub Actions YAML | actionlint exit 0 | v1.7.12 accepted workflow; release archive SHA-256 verified |
| Dependabot YAML | Parse successfully | Parsed with PyYAML BaseLoader (avoids YAML 1.1 `on` coercion) |
| Markdown | Valid local inline links/fragments and balanced fences | Checked by [check_docs.py](../scripts/check_docs.py); final counts in JSON |
| External Markdown destinations | HTTP success after redirects | 7 of 9 returned HTTP 200; both ISO pages returned 403 to curl, so automated availability was not established |
| Whitespace | `git diff --check` exit 0 | Passed |
| Existing screenshots/demo | No binary/source changes | Verified against baseline |
| Hosted PR workflow | Successful execution on Ubuntu/Python 3.12 | Pending PR creation at this evidence stage; local success is not hosted evidence |

## Historical and repository-setting verification

- [Successful historical run](https://github.com/napol-n/iso27001-secure-cicd/actions/runs/32397220447):
  successful scanner step; log corroborates original clean screenshot.
- [Historical failed run](https://github.com/napol-n/iso27001-secure-cicd/actions/runs/32396024034):
  failure conclusion, zero jobs returned. Root cause unverified; not detection evidence.
- `GET /repos/napol-n/iso27001-secure-cicd/branches/main/protection` returned
  **404 “Branch not protected”**. `GET /repos/napol-n/iso27001-secure-cicd/rules/branches/main`
  returned **[]**. These observations are time-specific and do not assess account-level
  security or future settings.
- Full-SHA references for checkout v7.0.1, setup-python v7.0.0, and upload-artifact
  v7.0.2 were resolved through upstream GitHub tag APIs. SHA pinning follows
  [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

## Changed-file summary

| Files | Purpose |
|---|---|
| `README.md` | Professional portfolio entry point and Mermaid architecture |
| `security/secret_scan.py`, `security/README.md` | Expanded scanner, documented contract, limitations and established-scanner decision |
| `tests/test_secret_scan.py`, `tests/test_security_tools.py`, `pytest.ini` | Synthetic regression and gate tests |
| `requirements-dev.txt`, `.gitignore` | Pinned direct tooling and local-output hygiene |
| `.github/workflows/security.yml`, `.github/dependabot.yml` | Enforced CI commands, least privilege, pinned Actions, evidence artifact and update cadence |
| `grc/scope.md`, `grc/asset-inventory.md` | Accurate implemented/scenario boundaries and ownership |
| `grc/risk-register.md`, `grc/risk-treatment.md` | Preserved original risk plus additional risks, treatment milestones and acceptance status |
| `grc/control-mapping.md`, `grc/statement-of-applicability.md`, `grc/control-effectiveness.md` | Selected ISO mapping and testable effectiveness criteria |
| `scripts/check_docs.py` | Offline local Markdown link/fragment/fence validation |
| `evidence/README.md`, `evidence/test-results.md`, `evidence/validation-report.md` | Evidence index, corrected observations, validation and gaps |
| `evidence/local-validation.json`, `evidence/dependency-audit.json`, `evidence/pytest.xml` | Actual captured local execution artifacts |

`app/app.py` and both screenshots are preserved byte-for-byte.

## Remaining risks and verification limits

- RISK-001: provisional **10 High**; no history scan, pre-push prevention, complete
  detection, real secret manager, or credential-rotation verification.
- RISK-002: provisional **8 Medium**; known-advisory/static-pattern limits,
  unpinned transitives, and no remediation process performance evidence.
- RISK-003: **15 High**; required merge checks, independent review, and restricted
  bypass remain unimplemented. A negative blocked-merge test was not performed.
- No live customer web application, production deployment, penetration test,
  independent assurance, management risk acceptance, or full ISMS evaluation.
- Windows/Python versions other than those stated are not verified. Tests deliberately
  use POSIX file features. actionlint is a local validation tool, not a CI dependency.
  ShellCheck was not installed, so actionlint's optional ShellCheck integration was
  not exercised; the workflow commands were run directly during validation.
- Documentation checker covers the repository's inline Markdown links, headings,
  and fences, not arbitrary HTML/reference-link syntax or external availability.
  All nine external inline destinations were requested separately; ISO's two
  destinations returned HTTP 403 to curl (their official pages were also consulted
  through browser search). Visual Mermaid rendering was not verified.
- Initial restricted-network audit failed on DNS. This was not treated as a clean
  audit; network-enabled runs provided the dependency observations.

See [effectiveness criteria](../grc/control-effectiveness.md) and
[treatment actions](../grc/risk-treatment.md) before revising residual risk estimates.
