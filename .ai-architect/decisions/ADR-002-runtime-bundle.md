---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-002
  title: Desktop Commander OSS and Supergateway as one tool unit
  status: accepted
  context: The existing pilot bundles the open-source MCP server with a stdio-to-HTTP
    bridge.
  drivers:
  - Preserve verified structure
  - Avoid new orchestration layers
  considered_option_ids:
  - OPT-003
  - OPT-004
  selected_option_id: OPT-003
  decision: Keep Desktop Commander OSS and its small configurable Supergateway bridge
    together, with pinned versions and runtime-configurable MCP listener, port and
    path.
  positive_consequences:
  - Fewer moving parts and a familiar local MCP endpoint
  negative_consequences:
  - Both processes share one container lifecycle; bridge configuration needs an entrypoint
  assumptions:
  - Versions used by existing pilot are a starting point, not yet a vetted public
    release
  validation_criteria:
  - MCP initialize, tools/list, and an authorized tools/call pass over HTTP; process
    failure is reported
  supersedes: []
---

# ADR-002: Desktop Commander OSS and Supergateway as one tool unit

**Status:** Accepted

## Context
The existing pilot bundles the open-source MCP server with a stdio-to-HTTP bridge.

## Drivers
- Preserve verified structure
- Avoid new orchestration layers

## Considered options
- OPT-003: one container for Desktop Commander OSS plus Supergateway
- OPT-004: separate microcontainers for each process

## Decision
Keep Desktop Commander OSS and its small configurable Supergateway bridge together, with pinned versions and runtime-configurable MCP listener, port and path.

**Selected option:** OPT-003

## Consequences
**Positive**
- Fewer moving parts and a familiar local MCP endpoint

**Negative**
- Both processes share one container lifecycle; bridge configuration needs an entrypoint

## Assumptions
- Versions used by existing pilot are a starting point, not yet a vetted public release

## Validation criteria
- MCP initialize, tools/list, and an authorized tools/call pass over HTTP; process failure is reported
