# Information Security Risk Register

## Purpose

This risk register identifies and evaluates information security
risks within the NovaTech software development and CI/CD scope.

---

## Risk Assessment Methodology

Risk is evaluated using two factors:

- Likelihood: Probability that the risk event will occur
- Impact: Potential consequence if the risk event occurs

Risk Score is calculated as:

Risk Score = Likelihood × Impact
## Likelihood Scale

| Score | Rating | Description |
|---|---|---|
| 1 | Rare | The event is highly unlikely to occur |
| 2 | Unlikely | The event could occur but is not expected |
| 3 | Possible | The event may occur under normal circumstances |
| 4 | Likely | The event is expected to occur periodically |
| 5 | Almost Certain | The event is expected to occur frequently |
## Impact Scale

| Score | Rating | Description |
|---|---|---|
| 1 | Insignificant | Minimal security or business impact |
| 2 | Minor | Limited impact with easy recovery |
| 3 | Moderate | Noticeable operational or security impact |
| 4 | Major | Significant operational, financial, or security impact |
| 5 | Severe | Severe security, legal, financial, or business impact | 
## Risk Rating Criteria

| Risk Score | Rating |
|---|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

---

# Risk Register

## RISK-001 — Hardcoded Credential Exposure

**Affected Assets:**

- AST-001 — Application Source Code
- AST-002 — GitHub Repository
- AST-003 — API Credentials and Secrets

**Threat:**  
Credential exposure

**Vulnerability:**  
The development process does not currently include automated
secret detection before code integration.

**Risk Event:**  
A developer may accidentally commit a hardcoded credential
to the source code repository.

**Potential Impact:**

- Unauthorized access to systems or services
- Exposure of sensitive information
- Abuse of API or service privileges
- Potential financial or operational impact

**Risk Statement:**

Due to the absence of automated secret detection, developers may
commit hardcoded credentials to the source code repository,
potentially resulting in credential exposure and unauthorized
access to systems or services.

**Likelihood:** 3 — Possible

**Impact:** 5 — Severe

**Risk Score:** 15

**Risk Rating:** High 

## Risk Summary

| Risk ID | Risk | Likelihood | Impact | Score | Rating |
|---|---|---:|---:|---:|---|
| RISK-001 | Hardcoded Credential Exposure | 3 | 5 | 15 | High |

## Risk Acceptance Criteria

| Rating | Decision |
|---|---|
| Low | Acceptable |
| Medium | Acceptable with monitoring |
| High | Risk treatment required |
| Critical | Immediate risk treatment required |
