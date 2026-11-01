---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-001
  title: Independent public identity and upstream attribution
  status: accepted
  context: A public distribution must be usable beyond a particular laptop, organization
    or paid product.
  drivers:
  - Vendor neutrality
  - Avoid confusion with commercial Remote Desktop Commander
  considered_option_ids:
  - OPT-001
  - OPT-002
  selected_option_id: OPT-001
  decision: Use the project name Workstation MCP Bridge and the proposed repository
    aldo80st/workstation-mcp-bridge. Upstream component references are factual attribution,
    not endorsement.
  positive_consequences:
  - Users can evaluate a provider-neutral MCP bridge
  negative_consequences:
  - Name clearance, trademark, and distribution license checks remain necessary
  assumptions:
  - No commercial publication is authorized solely by architectural approval
  validation_criteria:
  - README/NOTICE attribute upstream components; no third-party branding implies official
    affiliation
  supersedes: []
---

# ADR-001: Independent public identity and upstream attribution

**Status:** Accepted

## Context
A public distribution must be usable beyond a particular laptop, organization or paid product.

## Drivers
- Vendor neutrality
- Avoid confusion with commercial Remote Desktop Commander

## Considered options
- OPT-001: workstation-mcp-bridge independent name
- OPT-002: Desktop Commander branded fork

## Decision
Use the project name Workstation MCP Bridge and the proposed repository aldo80st/workstation-mcp-bridge. Upstream component references are factual attribution, not endorsement.

**Selected option:** OPT-001

## Consequences
**Positive**
- Users can evaluate a provider-neutral MCP bridge

**Negative**
- Name clearance, trademark, and distribution license checks remain necessary

## Assumptions
- No commercial publication is authorized solely by architectural approval

## Validation criteria
- README/NOTICE attribute upstream components; no third-party branding implies official affiliation
