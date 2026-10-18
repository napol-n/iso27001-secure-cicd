# Control Effectiveness Assessment

## Basis and decision rules

This is a maintainer-performed portfolio assessment, not an independent audit.
Review date and observed runs are recorded in the [validation report](../evidence/validation-report.md).
Owners are fictional roles. **Implemented** means code/configuration exists;
**tested** means a specified procedure was observed; neither implies full ISO
compliance. Assess operating effectiveness only within the tested boundary.

## CTRL-001 — Automated Secret Detection

- **Objective/risk:** Detect selected hardcoded secrets and fail incomplete scans;
  address RISK-001 across AST-001/002/003.
- **Owner:** DevOps Team; Development Team owns the risk.
- **Implementation evidence:** [Scanner](../security/secret_scan.py),
  [workflow](../.github/workflows/security.yml), [tests](../tests/test_secret_scan.py).
- **Testing procedure:** Run pytest, scan clean application and whole repository,
  then run CLI against temporary synthetic secret and invalid-encoding files.
  Inspect stdout/stderr for value disclosure. Test multiple findings, file formats,
  exclusions, unreadable files/directories, symlinks, and actual process exit codes.
- **Effectiveness criteria:** Clean eligible input exits 0; configured secret inputs
  exit 1; incomplete/empty scans exit 2; tested matched values never appear in output.
  All regression assertions pass; each negative fixture fails for the intended reason.
- **Assessment:** See [observed results](../evidence/test-results.md). Effective only
  for tested patterns and file handling. The historical failed screenshot does not
  establish control operation. Post-push detection cannot prevent initial exposure.
- **Residual risk:** RISK-001 stays 10 High (provisional); false negatives, excluded
  content/history, and bypass remain.
- **Recommended improvements:** Maintained scanner, history scan, push protection,
  secret manager, rotation procedure, and required merge checks before production use.

## CTRL-002 — Python Static Analysis

- **Objective/risk:** Detect selected unsafe Python constructs; address RISK-002.
- **Owner:** Development Team.
- **Implementation evidence:** Bandit command in [workflow](../.github/workflows/security.yml);
  [tool pin](../requirements-dev.txt).
- **Testing procedure:** Scan `app`, `security`, `scripts`; run the same command on a
  temporary synthetic unsafe `eval` example. Use metadata-only output.
- **Effectiveness criteria:** Current scoped code exits 0; negative fixture exits
  nonzero with the intended Bandit rule. No source lines appear in the report.
- **Assessment:** Bounded static-analysis gate; observations in [validation](../evidence/validation-report.md).
  Test code is excluded because it intentionally creates insecure cases and uses
  assertions/subprocesses. The custom secret gate still includes tests.
- **Residual risk:** Contributes to provisional RISK-002 score 8 Medium; no assurance
  against all logic flaws, runtime vulnerabilities, or malicious code.
- **Recommended improvements:** Independent review and application-specific security
  tests when a real application exists; triage findings rather than weakening thresholds.

## CTRL-003 — Dependency Vulnerability Assessment

- **Objective/risk:** Detect published vulnerabilities in installed CI tools and
  transitive Python packages; address RISK-002/AST-006.
- **Owner:** DevOps Team.
- **Implementation evidence:** pip-audit and weekly scheduled workflow;
  [Dependabot](../.github/dependabot.yml).
- **Testing procedure:** Audit the isolated installed environment with `--strict`;
  separately audit a temporary known-vulnerable requirement using `--no-deps
  --disable-pip` so that the package is not installed.
- **Effectiveness criteria:** Current environment has no reported advisory and exits
  0; negative requirement produces a vulnerability finding/nonzero exit. Network or
  collection errors must fail the job rather than being relabeled clean.
- **Assessment:** Time-specific known-advisory check; see [validation](../evidence/validation-report.md).
  The application itself has no external runtime dependencies. No production
  vulnerability-management process or remediation performance is demonstrated.
- **Residual risk:** RISK-002 8 Medium is provisional; unknown/malicious packages,
  unpinned transitives, and advisory availability remain.
- **Recommended improvements:** Review update PRs, define remediation targets, and
  consider a hashed lockfile if dependency scope grows.

## CTRL-004 — Controlled CI Changes

- **Objective/risk:** Limit workflow privileges and maintain reviewable changes;
  address RISK-003 and support RISK-001.
- **Owner:** Repository Owner / DevOps Team.
- **Implementation evidence:** Dedicated branch/PR, full-SHA action references,
  `contents: read`, disabled checkout credential persistence, timeouts,
  [workflow](../.github/workflows/security.yml).
- **Testing procedure:** Validate YAML with actionlint; verify pins against upstream
  tags; inspect GitHub branch protection and applicable rules; inspect hosted job
  conclusions. A future test must attempt to merge a deliberately failing PR.
- **Effectiveness criteria:** Valid workflow and correct nonzero propagation;
  main cannot accept a failing/unreviewed change under configured repository rules.
- **Assessment:** Configuration is partial. Repository settings did not enforce
  required checks at review. A blocked-merge test has **not** been performed.
- **Residual risk:** RISK-003 remains 15 High; the control does not yet meet its
  merge-enforcement objective.
- **Recommended improvements:** Require `Security checks`, independent approvals,
  restrict bypass, and protect workflow/control changes. Keep this risk open until
  settings and negative merge tests provide evidence.
