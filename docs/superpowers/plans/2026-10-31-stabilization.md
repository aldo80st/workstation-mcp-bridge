# v0.1 stabilization implementation plan

> Execute inline with superpowers:executing-plans; user explicitly authorized autonomous implementation against existing ADRs.

**Goal:** A reproducible isolated ARM64 pilot with verified Restricted/Open behavior and optional tunnel.
**Architecture:** Preserve Desktop Commander 0.3.1 and Supergateway 4.2.1 in one container; optional tunnel 0.0.19. Follow ADR-001..005 and architecture-contract revision 1.
**Spec:** User execution request and .ai-architect/architecture-contract.yaml.

## Constraints
No changes to existing pilots or homelab. No main merge or stable release. Synthetic workspaces; no credentials in evidence. Keep ports loopback. ARM64 local and AMD64 CI evidence are distinct.

## Review focus
Outside-workspace reads (absolute, traversal, symlink, multiple files); misleading health; malformed paths/ports; missing bind sources; tunnel overrides and secret-file startup.

### Task 1: Baseline and regression tests
- [ ] Save system/Compose/image baseline; build original pinned dependencies.
- [ ] Reproduce outside-workspace reads through real MCP; add negative regression tests.
- [ ] Add Compose tests for missing workspace and configurable tunnel backend.

### Task 2: Runtime corrections
- [ ] Configure Desktop Commander workspace path policy at startup, retaining container isolation as host boundary.
- [ ] Use Supergateway server health, validate endpoint paths and prevent bind source creation.
- [ ] Permit tunnel backend override and test real pinned CLI with synthetic identity/key.
- [ ] Run tests, restart/profile switching and rollback in isolated Compose project.

### Task 3: Security, delivery and installation
- [ ] Run scans and SBOM tied to image ID; classify findings without blanket suppressions.
- [ ] Document usage, operations, limitations and actual compatibility.
- [ ] Review complete diff; fix significant findings with RED/GREEN tests.
- [ ] Commit and create reviewable PR, inspect fresh CI; install isolated pilot if runtime checks pass.
- [ ] Record unmet acceptance criteria; do not call sprint complete.

## Execution ledger

- Baseline: Ubuntu ARM64, Docker permission intervention resolved via user-applied temporary ACL; occupied 8765 preserved, isolated validation port 18795.
- RED/GREEN: outside-workspace reads, tunnel backend override, missing bind sources, secret-reader UID, reserved/control/dot endpoint paths, Open failure cleanup.
- Final review: independent subagent source/evidence review; two P2 findings and one CI proof gap addressed.
- Final local verification: 10 pytest, 11 Restricted MCP, 8 startup, 4 Open tests passed; restart/stop/start/profile return passed. Full output retained outside git.
- Security: final image scan/SBOM retained; 43 HIGH remain, no blanket waiver. npm audit independently flags 3 HIGH entries.
- Ruling: no restart of the host Docker daemon while unrelated active containers are present; maintenance-window approval is still required to establish that acceptance criterion. Container restart/stop/start is verified and explicitly distinguished.
- No main merge or stable publication. Real tunnel credentials/target workspace selection remain external E2E prerequisites.
