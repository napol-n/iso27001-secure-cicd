# Statement of Applicability

## Purpose

This document records the applicability of selected ISO/IEC 27001:2022
Annex A controls relevant to the NovaTech secure software development
and CI/CD scope.

This is a limited Statement of Applicability created for the scope of
this portfolio project and does not represent a complete organizational
ISO/IEC 27001 Statement of Applicability.

---

## Applicable Controls

| Control | Applicable | Justification | Implementation | Evidence |
|---|---|---|---|---|
| A.8.25 Secure Development Life Cycle | Yes | NovaTech develops application software and security requirements must be integrated into the development lifecycle. | Security checks integrated into GitHub Actions CI workflow. | `.github/workflows/security.yml`, GitHub Actions results |
| A.8.28 Secure Coding | Yes | Hardcoded credentials represent an insecure coding practice and create credential exposure risk. | Python secret detection control checks application source code. | `security/secret_scan.py`, TEST-001, TEST-002 |
| A.8.29 Security Testing in Development and Acceptance | Yes | Application source code requires automated security testing before integration. | Secret detection executes automatically during CI/CD events. | GitHub Actions workflow logs and test evidence |
| A.8.32 Change Management | Yes | Changes to application source code may affect security and must be managed through controlled version changes. | Git version control, branches, commits, and pull requests. | Git commit history and pull request records |
