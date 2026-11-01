# Workstation MCP Bridge v0.1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an independent, provider-neutral, safe-by-default Workstation MCP Bridge v0.1 that supports Linux ARM64/AMD64, local MCP, optional outbound OpenAI tunnel, and explicit Restricted/Open profiles verified by independent tests.

**Architecture:** Bundle Desktop Commander OSS and Supergateway as a single configurable tool runtime; make every connection adapter optional. Every client request must traverse effective policy enforcement before reaching MCP tooling; container filesystem mounts remain the host boundary. No backend redesign, no proprietary Desktop Commander components.

**Tech Stack:** Docker/Compose, OCI Linux images, Desktop Commander OSS, Supergateway, MCP Streamable HTTP/stdio where tested, optional OpenAI tunnel-client; GitHub Actions, MCP Inspector, test harness (Python/pytest recommended), Trivy, Gitleaks, Syft, ShellCheck, Hadolint, optional Grype/CodeQL/Scorecard.

**Spec:** `.ai-architect/architecture-contract.yaml` revision 1 and `.ai-architect/decisions/ADR-001`.. `ADR-005`; architectural implementation baseline: `.ai-architect/implementation-plan.md`.

**Sprint:** [tracking #1](https://github.com/aldo80st/workstation-mcp-bridge/issues/1) · Staging plan branch `docs/sprint-v0.1-plan` · 2026-10-31. Planned work only; no application code, image or live tunnel deployed yet.

## Global Constraints

- Restricted is **default**: effective deny of unauthorized `tools/call` and no route that bypasses the policy; hiding `tools/list` entries alone is insufficient (ADR-003, Q-001).
- Open is **explicit opt-in** with a warning; it changes only user-authorized mount/permission scope, never grants unauthenticated Internet access (ADR-003).
- Desktop Commander OSS + Supergateway share one runtime container; adapters remain separate and optional; local core works without OpenAI (ADR-002, ADR-004).
- No privileged mode, `docker.sock`, whole-host `/`, host-wide HOME, secrets baked into images or committed credentials (ADR-005).
- Pin image versions/digests; verify actual upstream CLI and licenses (do not assume placeholder environment variables map to upstream flags).
- Linux/amd64 and Linux/arm64 get actual clean runtime checks, not build-only badges; supported provider claims require true E2E evidence.
- Do not alter running homelab/XPS deployments without explicit authorization; no release publication before Q-001 and Q-003 are resolved (Q-002 required if tunnel is in release).
- GitHub: isolated task branch + PR, independent review, visible commands/logs, fresh verification on the final SHA before marking a task done.

## Delivery order / gates

| Stage | Issues | Dependencies | Gate |
| --- | --- | --- | --- |
| S0 / discovery | #2, #3, #4 | ADRs/contracts | Q-001 architecture solution + Q-003 licensing (can progress in parallel) |
| S1 / runtime | #5, #6, #7 | #2 | working and verified local MCP / least-privilege Docker |
| S2 / profiles | #8, #9 | #3, #5–#7 | no bypass for Restricted; Open deliberate |
| S3 / adapters | #10, #11, #12 | #7–#9 | provider-neutral local path; OpenAI optional, real-client matrix |
| S4 / independent verification | #13, #14, #15 | tested components | verified ARM64/AMD64, abuse tests, recovery |
| S5 / release candidate | #16 | #4, #8–#15 | documented go/no-go |

**Critical path:** #2 → #3 → #8 → #14 → #16, joined by #4 (licenses) and #13 (CI). S1 runtime work can proceed independently of policy-spike research, but cannot ship Restricted without #3 and #8.

## Review Focus — failures not always obvious from a spec

1. Direct calls to backend HTTP bypass policy → #8 negative E2E reaches no tool and changes no file.
2. Symlink/path traversal or shell command escapes workspace → #6 and #8 read/write/command denial tests.
3. Open profile flips on without conscious acknowledgement → #9 rejects missing acknowledgement and unsafe networking.
4. Missing/misformatted tunnel key causes secrets to appear in stdout/compose/config → #11 and #13 sentinel-key leak tests.
5. Service restart/reconnect silently loses protocol readiness or breaks local mode → #7, #11 and #15 fresh initialize/tools/list/tools/call after disruption.

---

### Task 1: Audit actual baseline, license and outstanding architectural decisions — #2, #4

**Files:** Modify `.ai-architect/project-context.md`; create `docs/upstream-evidence.md`, `docs/legal-review.md`; create/modify `NOTICE.md`, `SECURITY.md`, `LICENSE` only after verification.

**Interfaces:** Consumes ADR-001/ADR-005 and upstream documentation; produces recorded versions/digests and publication constraints for #5/#11/#16.

- [ ] **Step 1:** Confirm repo is public; README and ADRs exist; locate all bundled licenses from upstream primary sources and record links+dates.
- [ ] **Step 2:** Record verified upstream runtime/transport versions, image architectures and a timestamp; do not infer availability from the existing Ubuntu pilot.
- [ ] **Step 3:** Correct stale project-context assertions (repo already exists; no runtime implementation).
- [ ] **Step 4:** Draft independent-brand notices and supply-chain obligations; identify what requires legal review.
- [ ] **Step 5:** PR review ensures no credentials, non-OSS material or unexplained claimed vendor endorsement.

### Task 2: Resolve the security policy engine choice — #3

**Files:** Create `docs/security-enforcement-decision.md`, `tests/security/test_policy_gateway.py` (isolated fixture), and a superseding ADR only if the accepted contract must change.

**Interfaces:** Input: MCP HTTP requests, identity and policy; output: an enforced allow/deny response with **no executable bypass path**. Candidate mechanism must be a vetted existing product/library, not a new platform.

- [ ] **Step 1:** Collect official version-specific authorization capabilities and known upstream defects for candidate gateways (compare with local app's needs).
- [ ] **Step 2:** Write a negative fixture calling a prohibited `tools/call` with a synthetic file mutation and an allowed read case.
- [ ] **Step 3:** Run the fixture against policy disabled to see the prohibited mutation (RED) in an isolated sandbox.
- [ ] **Step 4:** Configure candidate policy so direct forbidden call rejects and permitted read succeeds (GREEN); verify no backend HTTP route bypasses it.
- [ ] **Step 5:** Capture sanitized transcripts, list residual weaknesses, decide go/no-go; request ADR amendment if architecture changes.

### Task 3: Build the vendor-neutral runtime image — #5

**Files:** Create `images/workstation-mcp/Dockerfile`, `images/workstation-mcp/entrypoint.sh`, `compose.yaml`, `.env.example`, `.gitignore`, `tests/runtime/test_entrypoint.py`.

**Interfaces:** Consumes `MCP_PORT`, `MCP_PATH`, `WORKSPACE_PATH` and pinned version metadata; exposes container-internal `mcp-http` with stdio bridged to Desktop Commander OSS.

- [ ] **Step 1:** Test invalid port/path/config and absent workspace: startup fails clearly without leaking paths/keys; verify initial FAIL.
- [ ] **Step 2:** Implement minimal validated entrypoint using installed, pinned packages (not runtime `npx -y` downloads); verify test PASS.
- [ ] **Step 3:** `docker compose config --quiet` and fresh clean OCI build pass with pinned versions.
- [ ] **Step 4:** Confirm process supervision, nonzero exit when bridge crashes and SIGTERM handling.
- [ ] **Step 5:** Commit PR with image digest, environment example and version provenance.

### Task 4: Enforce Docker host isolation and network boundaries — #6

**Files:** Modify `compose.yaml`; create `tests/security/test_host_isolation.py`, `scripts/doctor.sh`.

**Interfaces:** Input workspace host path and access mode `ro|rw`; output explicitly isolated volume and host loopback endpoint.

- [ ] **Step 1:** Create throwaway mounted/unmounted host fixture directories; test forbidden file read and privileged permissions as negative baseline (RED on insecure fixture).
- [ ] **Step 2:** Apply least-privilege UID/GID, cap_drop, no-new-privileges, explicit mounts and loopback binding.
- [ ] **Step 3:** Verify outside-mount read/write fails, readonly write fails, allowed fixture write works in rw; LAN reachability denied.
- [ ] **Step 4:** Inspect effective Compose and container mounts/network in tests, ensure no `docker.sock`, `/`, `host` network or privileged default.
- [ ] **Step 5:** Retest on clean environment and commit only confirmed evidence.

### Task 5: Build MCP protocol acceptance suite — #7

**Files:** Create `tests/mcp/test_contract.py`, `tests/fixtures/workspace/README.txt`, `scripts/test-mcp-local.sh`.

**Interfaces:** Input local Streamable HTTP MCP endpoint; expected output valid initialize, tools/list and an authorized tools/call with observable fixture result.

- [ ] **Step 1:** Write failing tests for handshake/session, malformed JSON-RPC, wrong headers and unsupported tool name.
- [ ] **Step 2:** Make implementation comply (RED→GREEN) without extending vendor-specific server behavior.
- [ ] **Step 3:** Test tools/list schema and tools/call using fixture while optional tunnel client is absent.
- [ ] **Step 4:** Pin and run MCP Inspector CLI in CI in addition to own test client; record exact verified command.
- [ ] **Step 5:** Retest after restart; capture status codes and response snippets without secrets.

### Task 6: Implement Restricted with active per-call deny — #8

**Files:** Create `config/restricted.example.yaml`, `tests/security/test_restricted.py`, gateway configuration files selected by #3.

**Interfaces:** Inputs authorization identity, MCP tool name and arguments; output allow/reject **before** stdio execution.

- [ ] **Step 1:** Write failing test that direct `tools/call` of denied command/write does not execute or create sentinel file.
- [ ] **Step 2:** Configure real enforcement policy from #3; no separate direct route to unguarded Supergateway.
- [ ] **Step 3:** Verify allowed read in fixture and denied direct call (RED→GREEN). Hiding tool discovery is not acceptance.
- [ ] **Step 4:** Negative tests: path traversal, symlink escape, command execution workaround, invalid/empty policy, policy service outage.
- [ ] **Step 5:** Independent reviewer reproduces forbidden-call test and confirms no side-effect; block if bypass found.

### Task 7: Implement Open opt-in and reversible profile switch — #9

**Files:** Create `compose.open.yaml`, `config/open.example.yaml`, `tests/security/test_open_opt_in.py`, activation UX docs/script.

**Interfaces:** Input explicit user configuration + opt-in acknowledgement; output an expanded but defined set of mounts, not anonymous remote publication.

- [ ] **Step 1:** Test Open without explicit opt-in fails, and dangerous auto-mount settings are absent (RED).
- [ ] **Step 2:** Implement opt-in mechanism showing meaningful warning; no implicit `/` or `docker.sock`.
- [ ] **Step 3:** Verify expanded test workspace works and no network exposure beyond the configured trust boundary (GREEN).
- [ ] **Step 4:** Revert to Restricted; old paths are inaccessible and existing local MCP remains operational.
- [ ] **Step 5:** Record risk acknowledgement semantics in `SECURITY.md`.

### Task 8: Implement baseline local adapter and client guidance — #10

**Files:** Create `adapters/local/README.md`, `docs/providers.md`, `docs/getting-started.md`, `tests/integration/test_local_client.py`.

**Interfaces:** MCP Streamable HTTP loopback by default; optional stdio bridge only if verified with a real client.

- [ ] **Step 1:** Test local client initialization/list/call against container without outbound tunnel.
- [ ] **Step 2:** Document tested syntax for client configuration with synthetic path/IDs, no universal compatibility claim.
- [ ] **Step 3:** Prove disabling all optional adapters does not alter local MCP behavior; capture version/OS/mode.
- [ ] **Step 4:** Commit client-specific guidance only with run evidence.

### Task 9: Integrate optional OpenAI Secure MCP Tunnel — #11

**Files:** Create `adapters/openai-tunnel/compose.tunnel.yaml`, `adapters/openai-tunnel/README.md`, `tests/integration/test_tunnel_config.py`, `secrets/.gitignore`.

**Interfaces:** `CONTROL_PLANE_TUNNEL_ID`, `MCP_SERVER_URL`, protected key file (exact CLI path based on verified pinned version). Adapter contacts provider, not the tooling process directly; local stays working without this adapter.

- [ ] **Step 1:** Verify official tagged image, architecture support, current CLI/flags and secret-file semantics (Q-002).
- [ ] **Step 2:** Write test for missing ID/key, invalid format, unreachable endpoint, stale credentials; adapter should fail independently (RED).
- [ ] **Step 3:** Implement minimal opt-in Compose overlay and runtime secret file; unit tests PASS.
- [ ] **Step 4:** Scan logs, image layers and rendered config using sentinel secret value; never upload real key to GitHub or logs.
- [ ] **Step 5:** Authorize temporary external integration credentials for manual E2E; check readiness, reconnect and health.
- [ ] **Step 6:** Revoke test credentials and commit sanitized evidence.

### Task 10: Validate real MCP client compatibility matrix — #12

**Files:** Create `docs/compatibility-matrix.md`, `tests/integration/README.md`.

**Interfaces:** Each client row contains provider/client, version, OS, transport/auth, profile, test date, result and evidence link.

- [ ] **Step 1:** Define states `tested`, `not-tested`, `unsupported`, `blocked`; initial values are not-tested.
- [ ] **Step 2:** For each actual client credential/installation available, verify handshake/list/call and session lifecycle.
- [ ] **Step 3:** Test negative auth, reconnect and plugin/tool error path; do not infer compatibility from inspector alone.
- [ ] **Step 4:** Record gaps as issues; never fabricate vendor success.

### Task 11: Establish reproducible multi-architecture CI and supply-chain checks — #13

**Files:** Create `.github/workflows/ci.yml`, `.github/workflows/security.yml`, tests runner scripts; optional policy config.

**Interfaces:** PR SHA → checks for Docker/Compose, tests, Linux ARM64/AMD64 runtime, static lint, vulnerability, secrets, SBOM artifacts.

- [ ] **Step 1:** Write one intentionally failing fixture/config as proof a gate catches failure; run without real secrets.
- [ ] **Step 2:** Add Compose validation, ShellCheck, Hadolint, MCP Inspector contract run, tests and actual arch-specific execution.
- [ ] **Step 3:** Add Trivy, Gitleaks and Syft; Grype optionally for secondary scanning; CodeQL only if language supported; Scorecard advisory.
- [ ] **Step 4:** Pin GitHub Actions to SHAs with minimal `GITHUB_TOKEN` permissions; verify CI secrets not exposed to untrusted forks.
- [ ] **Step 5:** Fail gate on prohibited runtime config, regressions and severe actionable findings; document false-positive handling.
- [ ] **Step 6:** CI shows green only after fixing the intentionally failing fixture, and both architectures have real test evidence.

### Task 12: Independent adverse security review — #14

**Files:** Create `docs/security-review-v0.1.md`, adversarial fixtures under `tests/security/`; follow-up defect issues if needed.

**Interfaces:** Input release candidate tested in disposable workspace; output findings with severity, reproduction, fix and retest link.

- [ ] **Step 1:** Separate reviewer tests direct gateway bypass, prompt injection through synthetic files, symlink escape and shell abuse.
- [ ] **Step 2:** Validate Restricted deny is effective with tool names/JSON-RPC variants; retest on alternate architecture.
- [ ] **Step 3:** Inspect CI evidence, secrets in logs/image/config, unreviewed actions/third-party dependencies.
- [ ] **Step 4:** Open tracked defects and block release until critical/high exploitable defects resolved or explicitly risk-accepted.
- [ ] **Step 5:** Explicitly distinguish independent automated scanner findings from professional external penetration test.

### Task 13: Operational readiness and fault recovery — #15

**Files:** Create `scripts/setup.sh`, `docs/operations.md`, `docs/troubleshooting.md`, `docs/backup-rollback.md`, `tests/ops/`.

**Interfaces:** Input clean supported host and non-secret `.env`; output repeatable startup/readiness and safe rollback without data loss.

- [ ] **Step 1:** Write tests for failed preflight, occupied host port, no valid workspace path, missing key, network outage and container restart.
- [ ] **Step 2:** Implement non-destructive preflight and troubleshooting instructions; prove failure doesn't mutate host.
- [ ] **Step 3:** Execute fresh install, stop/start, rotate/disable tunnel, return to restricted; core stays functional.
- [ ] **Step 4:** Document reversibility without deleting mounted user content, including exact observed command outputs.

### Task 14: Candidate release and documented Go/No-Go — #16

**Files:** Create `CHANGELOG.md`, `docs/release-checklist.md`, versioned release notes, verified SBOM/checksums.

**Interfaces:** Inputs accepted PRs, CI results, license review, matrix and adversarial findings; output release candidate only when gates pass.

- [ ] **Step 1:** Verify all planned critical-path issues (#3/#4/#8/#13/#14) completed with reproducible evidence.
- [ ] **Step 2:** Execute clean deployment ARM64/AMD64; attach digests and complete log summaries, no exposed secrets.
- [ ] **Step 3:** Confirm official disclaimer, licenses, NOTICE, security contacts, SBOM, upgrade/rollback and tested-provider matrix.
- [ ] **Step 4:** Go/No-Go recorded; tag and publish only after explicit publication decision and checks.

## Definition of Done

A task is not done because a PR exists: it needs a fresh test command, exact result/exit code, appropriate negative and regression cases, independent review when required, and accepted PR. Document partial/blockers without claiming tests run. The whole sprint is not done unless the security boundaries, actual ARM64/AMD64 runs, third-party checks and publishability review are evidenced.

## Explicit non-goals

Do not implement a new orchestration/control-plane platform, promise arbitrary provider support, duplicate the homelab gateway, mount the host by default, run production migrations, or claim commercial-affiliation rights.

## Unresolved questions

- **Q-001 (blocks Restricted/release):** which audited existing policy enforcement point actually denies MCP `tools/call` without bypass?
- **Q-002 (blocks OpenAI adapter):** what pinned tunnel-client version and flags support runtime ID and secret-file authentication on both architectures?
- **Q-003 (blocks release):** can the selected project name and dependencies be redistributed with proper license/trademark notices?

**Execution mode after plan review:** Superpowers subagent-driven development is preferred for security-sensitive tasks with independent reviewers; fall back to sequential Codex task branches if independent subagents are unavailable. Planning approval does not itself authorize live production changes.
