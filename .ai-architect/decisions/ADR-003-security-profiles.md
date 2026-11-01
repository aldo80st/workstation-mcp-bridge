---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-003
  title: Explicit restricted and open security profiles
  status: accepted
  context: Desktop Commander exposes powerful filesystem and command tools; merely
    filtering tools/list or setting app options is insufficient.
  drivers:
  - Default secure configuration
  - Allow conscious advanced use
  - Boundary enforcement must be tested
  considered_option_ids:
  - OPT-005
  - OPT-006
  selected_option_id: OPT-005
  decision: Use restricted by default with minimal mounts, least-privilege UID, enforceable
    tool-call denies and no docker.sock. Open requires explicit opt-in and warnings;
    it expands only authorized mounts/permissions and never implies unauthenticated
    exposure.
  positive_consequences:
  - Safer onboarding and explicit risk acknowledgment
  negative_consequences:
  - A real policy enforcement mechanism must be validated or restricted cannot be
    declared safe
  assumptions:
  - Security controls must be tested against direct tools/call, not only tool discovery
  validation_criteria:
  - Negative tests deny forbidden tools and outside-path operations; open requires
    explicit configuration; no public anonymous endpoint
  supersedes: []
---

# ADR-003: Explicit restricted and open security profiles

**Status:** Accepted

## Context
Desktop Commander exposes powerful filesystem and command tools; merely filtering tools/list or setting app options is insufficient.

## Drivers
- Default secure configuration
- Allow conscious advanced use
- Boundary enforcement must be tested

## Considered options
- OPT-005: restricted default with guarded open opt-in
- OPT-006: always-open container

## Decision
Use restricted by default with minimal mounts, least-privilege UID, enforceable tool-call denies and no docker.sock. Open requires explicit opt-in and warnings; it expands only authorized mounts/permissions and never implies unauthenticated exposure.

**Selected option:** OPT-005

## Consequences
**Positive**
- Safer onboarding and explicit risk acknowledgment

**Negative**
- A real policy enforcement mechanism must be validated or restricted cannot be declared safe

## Assumptions
- Security controls must be tested against direct tools/call, not only tool discovery

## Validation criteria
- Negative tests deny forbidden tools and outside-path operations; open requires explicit configuration; no public anonymous endpoint
