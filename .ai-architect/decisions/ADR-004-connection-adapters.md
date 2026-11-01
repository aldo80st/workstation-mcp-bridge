---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-004
  title: Provider-neutral MCP transport and optional adapters
  status: accepted
  context: Some MCP clients use local stdio; others require HTTP or a vendor-specific
    outbound tunnel.
  drivers:
  - Client interoperability
  - No single vendor dependency
  considered_option_ids:
  - OPT-007
  - OPT-008
  selected_option_id: OPT-007
  decision: Keep MCP runtime independent. Provide local/HTTP MCP as the baseline and
    optional adapters for OpenAI tunnel, authenticated remote HTTP, or stdio client
    compatibility when validated for each provider.
  positive_consequences:
  - Users can connect different compatible MCP clients
  negative_consequences:
  - Not every MCP client supports all transports or auth; each integration requires
    evidence
  assumptions:
  - Direct tunnel compatibility is not a guarantee for third-party clients
  validation_criteria:
  - Baseline local initialize/tools/list/tools/call works without tunnel; adapter-specific
    e2e tests document supported clients
  supersedes: []
---

# ADR-004: Provider-neutral MCP transport and optional adapters

**Status:** Accepted

## Context
Some MCP clients use local stdio; others require HTTP or a vendor-specific outbound tunnel.

## Drivers
- Client interoperability
- No single vendor dependency

## Considered options
- OPT-007: neutral MCP HTTP core with optional connection adapters
- OPT-008: OpenAI tunnel mandatory for all uses

## Decision
Keep MCP runtime independent. Provide local/HTTP MCP as the baseline and optional adapters for OpenAI tunnel, authenticated remote HTTP, or stdio client compatibility when validated for each provider.

**Selected option:** OPT-007

## Consequences
**Positive**
- Users can connect different compatible MCP clients

**Negative**
- Not every MCP client supports all transports or auth; each integration requires evidence

## Assumptions
- Direct tunnel compatibility is not a guarantee for third-party clients

## Validation criteria
- Baseline local initialize/tools/list/tools/call works without tunnel; adapter-specific e2e tests document supported clients
