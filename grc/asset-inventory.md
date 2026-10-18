# Asset Inventory

The original NovaTech assets and CIA ratings are retained. Ratings represent the
fictional business scenario, not the sensitivity of this public portfolio. Owners
are simulated roles. Review at each material change and quarterly in the scenario.

| Asset ID | Asset | Type | Owner | Confidentiality | Integrity | Availability | Actual boundary and evidence |
|---|---|---|---|---|---|---|---|
| AST-001 | Application Source Code | Information | Development Team | High | High | Medium | Public demo in [app/](../app/app.py); security tooling in [security/](../security/secret_scan.py) |
| AST-002 | GitHub Repository | System | Development Team | High | High | High | Public Git history and PRs; no production data intended |
| AST-003 | API Credentials and Secrets | Information | DevOps Team | Critical | High | Medium | Scenario asset only; no real application credentials needed or stored; test data are synthetic |
| AST-004 | CI/CD Pipeline | System | DevOps Team | Medium | High | High | [Security workflow](../.github/workflows/security.yml); CI only, no deployment |
| AST-005 | Production Environment | System | Operations Team | High | Critical | Critical | Scenario-only downstream asset; no infrastructure or deployment evidence |
| AST-006 | Development and Security Dependencies | Software | DevOps Team | Low | High | Medium | [Pinned direct tools](../requirements-dev.txt); transitive versions resolved at installation |
| AST-007 | Risk Records and Test Evidence | Information | Security/GRC Lead | Low | High | Medium | [GRC records](risk-register.md), [evidence index](../evidence/README.md); metadata must not include credentials |

Credential classification describes the potential impact of a real exposure.
Screenshots and test reports are public portfolio artifacts; review before publication.
CI artifacts expire after 14 days; durable summaries in Git must identify the source
run, scope, and limitations. No backup or long-term evidence-retention control is
claimed. See [scope](scope.md) for system boundaries.
