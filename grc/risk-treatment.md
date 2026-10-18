# Information Security Risk Treatment Plan

## Treatment decisions

All owners and approval roles below are fictional. Status describes repository
implementation; it is not a claim of management authorization. No calendar deadlines
or approvals are invented. Proposed due milestones are tied to use of the control.

| Risk | Decision | Control/action | Owner | Status | Due/review milestone | Completion evidence |
|---|---|---|---|---|---|---|
| RISK-001 | Reduce | CTRL-001: retain Python gate; expand text/file coverage, redaction, and fail-closed errors | DevOps Team | Implemented; bounded tests available | Each change to rules or exclusions | [Scanner](../security/secret_scan.py), [tests](../tests/test_secret_scan.py), [results](../evidence/test-results.md) |
| RISK-001 | Reduce | Evaluate maintained scanner, history scan, and pre-commit/push protection | DevOps Team | Proposed; not active | Before real credentials or production use | Redacted history scan, exception review, prevention test required |
| RISK-001 | Reduce | Use a secret manager/environment injection; rotate any exposed real credential | Operations Team | Scenario recommendation; no live secrets | Before production use; immediately on exposure | Rotation/access review records required; none claimed |
| RISK-002 | Reduce | CTRL-002: Bandit SAST; CTRL-003: pip-audit of installed CI dependencies | DevOps Team | Implemented | Every PR, main push, and weekly scheduled run | [Workflow](../.github/workflows/security.yml), [validation](../evidence/validation-report.md) |
| RISK-002 | Reduce | Review Dependabot updates and dependency advisories | DevOps Team | Configuration added; human process pending | Weekly and on critical advisories | Reviewed update PRs; no remediation SLA performance claimed |
| RISK-003 | Reduce | CTRL-004: read-only workflow token, immutable action pins, no persisted checkout credentials | DevOps Team | Implemented configuration | Every workflow change | [Workflow](../.github/workflows/security.yml) |
| RISK-001, RISK-003 | Reduce | Require `Security checks` and independent PR review on main; restrict bypass and protect workflow changes | Repository Owner | Proposed; repository settings unchanged | Before relying on CI to prevent merges | Rules API plus a deliberately blocked test PR required |

## Expected technical behavior

- Clean eligible source: custom scanner exit 0.
- Simulated hardcoded secret: custom scanner exit 1 without revealing the value.
- Missing, unreadable, or unsupported target: custom scanner exit 2.
- Test assertion failure, Bandit finding, pip-audit advisory or audit error:
  nonzero command exit fails the workflow. Later checks can still collect evidence;
  no `continue-on-error` or forced-success option is configured.

A failed workflow is not equivalent to a blocked merge. Required repository rules
must be configured and tested separately. Tests of rejection use temporary synthetic
inputs; they must not introduce actual secrets or vulnerable installed packages.

## Residual risk and authorization

RISK-001 remains **10 High**, preserving the original estimate; further treatment
is required. RISK-002 is provisionally **8 Medium**, pending owner review. RISK-003
remains **15 High** until merge enforcement is implemented and tested. See the
[risk register](risk-register.md) for assumptions. The Development Team owns
RISK-001/RISK-003; the DevOps Team owns RISK-002. Simulated management must approve
the treatment plan and any exception; no acceptance/sign-off is recorded here.

Use the [effectiveness assessment](control-effectiveness.md) to decide whether
technical observations support a control's objective before revising residual risk.
