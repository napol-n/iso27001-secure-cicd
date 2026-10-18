# ISO/IEC 27001:2022 Control Mapping

## Risk → control → implementation → evidence

| Risk | Internal control | Relevant Annex A references | Implementation | Evidence and limits |
|---|---|---|---|---|
| RISK-001 | CTRL-001 Automated Secret Detection | A.8.25, A.8.28, A.8.29 | [Python scanner](../security/secret_scan.py), current-tree CI gate | [Tests and historical screenshots](../evidence/test-results.md); selected patterns only; no history scan |
| RISK-002 | CTRL-002 Python Static Analysis | A.8.25, A.8.28, A.8.29 | Bandit on app, security, scripts; all severities; metadata-only output | [Validation report](../evidence/validation-report.md); not complete code review or exploitability analysis |
| RISK-002 | CTRL-003 Dependency Vulnerability Assessment | A.8.8 | pip-audit of installed tools/transitives; weekly run; Dependabot configuration | [Workflow](../.github/workflows/security.yml), [validation](../evidence/validation-report.md); known advisories only; remediation ownership still needed |
| RISK-001, RISK-003 | CTRL-004 Controlled CI Changes | A.8.25, A.8.32 | Git branches/PRs, pinned Actions, read-only token, no persisted checkout credentials | [Workflow](../.github/workflows/security.yml), PR record; main merge enforcement is missing |

## Annex A reference titles and interpretation

| Reference | ISO/IEC 27001:2022 Annex A title | Contribution in this lab |
|---|---|---|
| A.8.8 | Management of technical vulnerabilities | Obtain known dependency vulnerability information; handling and remediation remain a process responsibility |
| A.8.25 | Secure development life cycle | Place repeatable checks into the development workflow |
| A.8.28 | Secure coding | Detect selected insecure patterns and discourage hardcoded credentials |
| A.8.29 | Security testing in development and acceptance | Exercise positive and negative cases and preserve test evidence |
| A.8.32 | Change management | Use versioned changes and PR review records; required review/merge enforcement remains incomplete |

These are supporting mappings, not assertions that a tool fully implements an Annex
A control. [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) defines ISMS
requirements; [ISO/IEC 27002:2022](https://www.iso.org/standard/75652.html) provides
control guidance. Annex A selection belongs in the context of risk treatment under
clause 6.1.3. Clause 6.1.2 informs risk assessment; clause 9.1 informs evaluation of
performance. This small project does not implement or assess all those requirements.

See the [selected-control SoA](statement-of-applicability.md), [assessment](control-effectiveness.md),
and [scope](scope.md). Original traceability is preserved:

**RISK-001 → CTRL-001 → A.8.25 / A.8.28 / A.8.29 → Python scanner → GitHub Actions → evidence → residual-risk review.**
