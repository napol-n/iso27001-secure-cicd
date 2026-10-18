# ISMS Scope — Portfolio Simulation

## Organization and business scenario

NovaTech is a fictional software company that develops and operates a Python-based
customer web application. In that scenario, a leaked API credential could expose
customer data, allow service abuse, and cause financial or operational harm.

## Implemented scope

This repository demonstrates security activities in the software development and
CI/CD process: source code, GitHub repository, security checks, development-tool
dependencies, change records, risk documentation, and test evidence.

The existing `app/app.py` is a runnable scanner demo, not an implemented customer
web application. The project preserves Python, Git, GitHub, and GitHub Actions.
There is no build artifact, deployment job, live customer data, or production
infrastructure. “CI/CD” describes the intended lifecycle; technical implementation
currently stops at CI security checks.

## Scenario scope and exclusions

The original scenario includes development and deployment processes and a production
environment. Deployment and AST-005 remain **scenario-only**; they are not tested
or claimed as implemented. Enterprise identity, physical security, HR controls,
legal obligations, incident operations, business continuity, and supplier assurance
are outside this repository's assessment. Excluded organizational areas are not
declared inapplicable to a real NovaTech ISMS.

## Assurance boundary

This is a limited portfolio simulation, not ISO/IEC 27001 certification, an audit
opinion, or a full ISMS implementation. Selected Annex A mappings explain how
technical controls support objectives. They do not demonstrate complete compliance
with those controls or clauses 4–10. All named teams are fictional accountability
roles; the repository maintainer performs the implementation and review exercises.
No management approval or formal residual-risk acceptance is asserted.
