# Evidence Index

Evidence demonstrates specific observations within the [portfolio scope](../grc/scope.md).
It is not an independent audit opinion or proof of ISO certification. Expected
behavior is documented separately from observed results; missing evidence remains
explicit. Do not publish credentials or raw secret-containing source lines.

| Evidence | Type and provenance | What it establishes |
|---|---|---|
| [Test results](test-results.md) | Maintainer review of historical runs and newly executed tests | Expected vs observed clean, rejected, and incomplete scans |
| [Validation report](validation-report.md) | Review context, checks, changes, and limitations | Scope of verification and unresolved controls |
| [Local validation JSON](local-validation.json) | Captured command results, UTC timestamp, source hashes | Reproducible local commands and their actual exit statuses |
| [Dependency audit JSON](dependency-audit.json) | pip-audit output after pip remediation | Package versions assessed and advisory results at execution time |
| [pytest XML](pytest.xml) | Actual local pytest JUnit output | Individual test cases and aggregate result |
| [Historical successful screenshot](screenshots/01-clean-pipeline-pass.png) | Original image retained without modification; commit b2bc679 | Visible workflow success, corroborated by historical scanner log |
| [Historical failed screenshot](screenshots/02-secret-detection-fail.png) | Original image retained without modification; commit d16d333 | Visible workflow failure only; no executed jobs returned by API |

The new tests do not replace the provenance of the old screenshots. No new screenshot
or hosted result is implied by a local test. Synthetic negative inputs are created
in temporary directories. pytest reports a passing test when the intended security
gate correctly rejects those inputs.

CI writes JUnit XML to `reports/pytest.xml` and uploads a run/attempt-named artifact
for 14 days. GitHub retains job logs according to repository retention settings.
The committed local XML/JSON is a durable snapshot, not an automatically refreshed
badge. Source hashes distinguish the tested implementation from later changes.
Review and refresh evidence after changing controls; include run URL, revision,
expected result, observed result, and any unavailable checks.
