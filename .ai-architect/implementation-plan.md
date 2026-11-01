# Architecture-Driven Implementation Plan

## Accepted decisions
ADR-001 through ADR-005; architecture-contract.yaml revision 1.

## Milestones

### M0 — Independent public-facing identity
**Outcome:** Document name, scope, attribution, supported transports and license obligations.
**Files/components:** README.md, NOTICE.md, SECURITY.md, LICENSE (only after license review), .gitignore.
**Constraints:** ADR-001, ADR-005.
**Dependencies:** Verify name/trademark position and upstream licenses before public publication.
**Verification:** Clear independent-project disclaimer; no embedded credentials or copyrighted commercial assets.

### M1 — Reproducible MCP tool unit
**Outcome:** Parameterized Desktop Commander OSS + Supergateway image, Compose default; ARM64/AMD64 when verified.
**Files/components:** compose.yaml, images/workstation-mcp/Dockerfile, entrypoint, .env.example.
**Constraints:** ADR-002, ADR-005; pin versions/digests; no default privileged mounts.
**Dependencies:** Reference pilot static files; do not alter existing running pilots.
**Verification:** Compose config passes; MCP initialize, tools/list and permitted tools/call work locally; test clean install and restart.

### M2 — Restricted enforcement and Open opt-in
**Outcome:** Enforce tool-call denial (not only discovery) plus scoped mounts and optional read-only workspace.
**Files/components:** security policy, restricted/open Compose overlays, SECURITY.md and tests.
**Constraints:** ADR-003; default restricted; open never means unauthenticated remote access.
**Dependencies:** Resolve Q-001 using an existing auditable gateway or equivalent enforcement; verify bypass cannot occur.
**Verification:** Direct forbidden tools/call fails; path traversal/outside-mount fails; open activation shows risk warning; tests prove host isolation. **Do not label restricted production-safe before these pass.**

### M3 — Optional connection adapters
**Outcome:** Local MCP core works independently; add opt-in OpenAI tunnel with tunnel ID and secret file; document HTTP/stdio clients.
**Files/components:** adapters/openai-tunnel, adapters/local, docs/providers.md, docs/runbook.md.
**Constraints:** ADR-004, ADR-005; no universal interoperability promises.
**Dependencies:** Pin tunnel-client release, confirm CLI/env/secret-file semantics and outbound connectivity.
**Verification:** Without tunnel, local MCP works. With test credentials, health/readiness and e2e MCP calls succeed; no secret appears in logs, image layers, or version control.

### M4 — Publication gate
**Outcome:** Public release candidate only after legal and security review.
**Files/components:** GitHub repository, CI, tagged release, user documentation.
**Constraints:** ADR-001 through ADR-005.
**Dependencies:** M0–M3; resolve Q-003.
**Verification:** Fresh ARM64/AMD64 test, negative security tests, verified provider matrix, trademark/license review and rollback procedure.

## Cross-cutting constraints
Keep shell access and filesystem permissions minimal; no implicit docker.sock, host root, privileged mode or Internet-exposed unauthenticated MCP; secrets only as non-versioned protected files; make tests observable; preserve existing pilots.

## Explicit non-goals
Do not implement a new orchestration platform or custom paid product imitation. Do not assert third-party client compatibility without validation. Do not publish a public repository or build images as a side effect of architecture approval.

## Unresolved questions
Q-001 blocks M2 shipping, Q-002 blocks OpenAI adapter in M3, Q-003 blocks M4 public publication.
