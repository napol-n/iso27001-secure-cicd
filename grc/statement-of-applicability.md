# Statement of Applicability — Selected-Control Portfolio Extract

This limited extract records selected Annex A controls relevant to the
[NovaTech simulation](scope.md). It is **not a complete organizational Statement of
Applicability**, a certification claim, or a full ISMS. It preserves the original
four selected controls and adds A.8.8 for dependency vulnerability assessment.

| Annex A control | Applicable in lab | Inclusion rationale | Implementation status | Evidence |
|---|---|---|---|---|
| A.8.8 Management of technical vulnerabilities | Yes | Known dependency vulnerabilities can compromise the development toolchain (RISK-002) | Partial: pip-audit and update configuration; remediation governance not demonstrated | [Workflow](../.github/workflows/security.yml), [validation](../evidence/validation-report.md) |
| A.8.25 Secure development life cycle | Yes | Security activities must accompany code changes (RISK-001/002/003) | Partial: automated CI gates; no deployed application or complete lifecycle policy | [Mapping](control-mapping.md), [workflow](../.github/workflows/security.yml) |
| A.8.28 Secure coding | Yes | Hardcoded credentials and unsafe Python constructs create exposure (RISK-001/002) | Partial: custom scanner and Bandit; no complete coding standard/training review | [Scanner](../security/secret_scan.py), [tests](../tests/test_secret_scan.py) |
| A.8.29 Security testing in development and acceptance | Yes | Selected security requirements need repeatable pass/fail tests | Partial: automated tests and CI; no penetration testing or production acceptance | [Test results](../evidence/test-results.md), [assessment](control-effectiveness.md) |
| A.8.32 Change management | Yes | Workflow and application changes can bypass or weaken checks (RISK-003) | Partial: Git and PRs; required status checks and independent approval not enforced | Git/PR history; [settings observation](../evidence/validation-report.md) |

## Unassessed controls and approvals

All other Annex A controls are **not assessed in this portfolio extract**. They are
not automatically excluded or deemed inapplicable. A complete organizational SoA
would determine necessary controls, record inclusion justification and implementation
status, and justify exclusions from Annex A in the context of clause 6.1.3 and the
organization's scope/risk treatment. This extract does not substitute for that work.

Prepared as a repository exercise; simulated Security/GRC Lead is the document owner.
Review at material scope/control changes and quarterly. No organizational approval
or risk-owner acceptance has been recorded. See the [risk treatment plan](risk-treatment.md).
