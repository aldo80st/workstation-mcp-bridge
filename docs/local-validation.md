# Local ARM64 validation — 2026-10-31

Environment: Ubuntu 26.10 ARM64, kernel 7.3.0-10-generic, Docker 29.7.2, Compose 2.40.3. Existing unrelated containers were preserved. Validation used its own Compose project and loopback port 18795.

Final image ID: `sha256:96fdfadc0343671fb16a7f272abd6b03f14be4bf9b3971f1304ef2b7a46b4203`. Desktop Commander 0.3.1, Supergateway 4.2.1; dependency versions/integrities in package-lock.json; Debian 13 multi-platform base pinned by digest.

- 10 pytest unit/configuration/orchestration tests passed.
- 11 Restricted MCP tests passed, including initialize, listing, allowed read, direct forbidden calls, alternate mutation tools, invalid JSON/method, canonical path/traversal/symlink/multiple-file denials.
- 8 container startup tests passed, covering invalid ports, unknown profile, Open without acknowledgement, missing API key file, invalid/control/dot/health-alias paths.
- 4 Open MCP tests passed; writes were read back and command output verified on the synthetic host workspace.
- Full Restricted suite passed after container restart, stop/start, and Open-to-Restricted recreation. Open workspace data remained intact.
- A deliberately failed Open test triggered cleanup and restored Restricted; unit regression also verifies failure cleanup.
- Health returned HTTP 503 when the MCP child executable failed. Normal initialize/ping health passed.
- tunnel-client 0.0.19 loaded a mode-0600 synthetic key with matching UID/GID, initialized the internal MCP server and retried a deliberately local failing control plane. Separate container-to-container initialize passed. No authorized OpenAI connection was attempted or claimed.
- ShellCheck 0.11.0, Hadolint 2.14.0 and Gitleaks 8.30.1 passed. Trivy 0.76.1: 0 CRITICAL, 43 HIGH, 69 MEDIUM, 60 LOW, 1 UNKNOWN. Syft 1.55.0 generated SPDX JSON. npm audit additionally reports 3 HIGH package-chain entries and 12 MODERATE; these are not silently waived.
- Public rulesets list was empty and public main branch metadata reported `protected: false`.

Independent code review found ambiguous endpoint paths, unsafe Open-test failure cleanup and insufficient tunnel secret startup proof. All three were addressed with reproductions/regressions or a real synthetic startup test. Reviewer could inspect source/evidence but could not run Docker from its sandbox; local execution evidence belongs to the implementation session.

Pending: fresh updated ARM64/AMD64 hosted CI, real ChatGPT tunnel E2E, actual Docker daemon restart/host reboot under a maintenance window that permits affecting other running containers, independent acceptance of vulnerability applicability and final license/brand distribution review. No sprint completion or stable release claim.

Private local evidence includes exact scanner reports, image metadata, SPDX SBOM, regression RED/GREEN outputs and lifecycle/tunnel logs. Do not publish raw deployment diagnostics or credentials. See security-findings.md and release-checklist.md.
