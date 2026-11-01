---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-005
  title: External secrets and host isolation
  status: accepted
  context: Reusable images must not contain tunnel identities, keys, paths or privileged
    host access.
  drivers:
  - Safe redistribution
  - Reproducible per-instance configuration
  - Limit blast radius
  considered_option_ids:
  - OPT-009
  - OPT-010
  selected_option_id: OPT-009
  decision: Parameterize tunnel ID and MCP URL. Supply tunnel API key from a read-only
    secret file if supported by installed client. Never bake credentials into images
    or commit files. Do not mount /, host home, or Docker socket by default.
  positive_consequences:
  - Same images are reusable on ARM64/AMD64 and across providers
  negative_consequences:
  - Secret file permissions and client image CLI must be verified per pinned release
  assumptions:
  - OpenAI tunnel is optional and its environment/CLI must be checked against actual
    selected version
  validation_criteria:
  - Secret material absent from logs and generated configs; container cannot access
    non-mounted host resources
  supersedes: []
---

# ADR-005: External secrets and host isolation

**Status:** Accepted

## Context
Reusable images must not contain tunnel identities, keys, paths or privileged host access.

## Drivers
- Safe redistribution
- Reproducible per-instance configuration
- Limit blast radius

## Considered options
- OPT-009: Compose environment plus file-mounted secret with least-privilege mounts
- OPT-010: baked image credentials and broad host mounts

## Decision
Parameterize tunnel ID and MCP URL. Supply tunnel API key from a read-only secret file if supported by installed client. Never bake credentials into images or commit files. Do not mount /, host home, or Docker socket by default.

**Selected option:** OPT-009

## Consequences
**Positive**
- Same images are reusable on ARM64/AMD64 and across providers

**Negative**
- Secret file permissions and client image CLI must be verified per pinned release

## Assumptions
- OpenAI tunnel is optional and its environment/CLI must be checked against actual selected version

## Validation criteria
- Secret material absent from logs and generated configs; container cannot access non-mounted host resources
