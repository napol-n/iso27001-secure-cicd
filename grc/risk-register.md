# Information Security Risk Register

## Purpose and assessment method

Assess risks in the [NovaTech simulation scope](scope.md). **Risk score = likelihood ×
impact**. Ratings are qualitative judgments, not measured probabilities. The
original RISK-001 scores and treatment context are retained. Reassess after a
material change, a new advisory/exposure, and quarterly in the scenario.

| Score | Likelihood | Description | Impact | Description |
|---|---|---|---|---|
| 1 | Rare | Highly unlikely | Insignificant | Minimal business impact |
| 2 | Unlikely | Could occur, but not expected | Minor | Limited impact; easy recovery |
| 3 | Possible | May occur under normal circumstances | Moderate | Noticeable operational/security impact |
| 4 | Likely | Expected periodically | Major | Significant operational/financial/security impact |
| 5 | Almost certain | Expected frequently | Severe | Severe security, legal, financial, or business impact |

| Score | Rating | Decision rule |
|---|---|---|
| 1–4 | Low | Eligible for documented owner acceptance |
| 5–9 | Medium | Eligible for owner acceptance with monitoring |
| 10–16 | High | Further treatment required; escalate to simulated management |
| 17–25 | Critical | Immediate treatment required |

A lower residual estimate is not approval. No owner or management acceptance has
been obtained in this portfolio. High residual risks remain open.

## RISK-001 — Hardcoded Credential Exposure

**Owner:** Development Team. **Assets:** AST-001, AST-002, AST-003.

**Threat/event:** A developer accidentally commits a credential, allowing an
unauthorized party to access systems, expose information, or abuse a service.
**Inherent vulnerability:** Before treatment, the process lacked automated secret
detection. **Current vulnerability:** The control has partial pattern and file
coverage, runs after push, and is not enforced by merge rules.

**Risk statement:** Without effective prevention and detection, hardcoded credentials
can enter the repository and expose systems or services. Scanning after push cannot
undo exposure, even if a subsequent integration check fails.

**Inherent:** likelihood 3 (Possible) × impact 5 (Severe) = **15, High**.
**Treatment:** reduce through CTRL-001, supported by CTRL-004.
**Residual:** likelihood 2 (Unlikely) × impact 5 (Severe) = **10, High**.

The original residual estimate is retained as a **provisional scenario judgment**:
tests demonstrate selected detection behavior, not an empirical likelihood reduction.
Impact remains Severe if a valid credential is exposed. No Git history scanning,
pre-push prevention, or required merge check is currently established. Further
treatment is required; this risk is **not accepted**.

## RISK-002 — Insecure Code or Vulnerable Dependencies

**Owner:** DevOps Team. **Assets:** AST-001, AST-004, AST-006.
**Threat/event:** An insecure Python construct or a dependency with a known
vulnerability is introduced into the development toolchain, enabling compromise.
**Vulnerability:** Manual review alone misses unsafe code; dependencies and advisory
data change over time. There are no third-party runtime application dependencies.

**Inherent:** 3 × 4 = **12, High**. **Treatment:** reduce with CTRL-002 and CTRL-003.
**Provisional residual:** 2 × 4 = **8, Medium**, pending owner review. Bandit and
pip-audit cover selected patterns and known published vulnerabilities. Unknown
vulnerabilities, malicious packages, unpinned transitive dependencies, and upstream
service availability remain relevant. No formal acceptance recorded.

## RISK-003 — Security Gate Bypass or Workflow Tampering

**Owner:** Development Team. **Assets:** AST-002, AST-004, AST-007.
**Threat/event:** A contributor changes the workflow/exclusions or merges failing
code, bypassing the intended security review.
**Vulnerability:** No branch protection or applicable branch rules were returned by
the GitHub API at review. Contributors can change the checks in the same PR.

**Inherent:** 3 × 5 = **15, High**. **Treatment:** reduce with CTRL-004 and required
independent review/merge rules. **Residual:** 3 × 5 = **15, High**, open. Read-only
tokens and action pinning limit workflow privileges and dependency drift, but do
not solve merge bypass. No likelihood reduction is claimed for that missing control.

## Consolidated risk summary

| Risk | Inherent L × I | Inherent | Controls | Residual L × I | Residual | Decision |
|---|---|---|---|---|---|---|
| RISK-001 | 3 × 5 | 15 High | CTRL-001, CTRL-004 | 2 × 5 | 10 High | Provisional; further treatment required |
| RISK-002 | 3 × 4 | 12 High | CTRL-002, CTRL-003 | 2 × 4 | 8 Medium | Provisional; owner review pending |
| RISK-003 | 3 × 5 | 15 High | CTRL-004 | 3 × 5 | 15 High | Open; merge enforcement missing |

See the [treatment plan](risk-treatment.md), [control mapping](control-mapping.md),
and [effectiveness assessment](control-effectiveness.md). Numerical residual scores
do not establish ISO conformity or independent control assurance.
