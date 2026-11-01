# Workstation MCP Bridge — Project context

Status: architecture accepted on 2026-10-31; no application implementation or GitHub publication.
Planned repository: `aldo80st/workstation-mcp-bridge` (not yet found as an accessible repository).

## Intent
Provider-neutral, containerized workstation MCP tools using Desktop Commander OSS with Supergateway; secure-by-default restricted and deliberate open profiles. Optional connection adapters include OpenAI tunnel.

## Existing pilot evidence
The reference pilot on Ubuntu ARM64 uses Desktop Commander OSS 0.2.43, Supergateway 4.2.1, HTTP `/mcp` on loopback port 8765, `~/labs` mount, and a separate SSH reverse-tunnel script. No integrated tunnel-client appears in the inspected Compose. These are reference observations, not public deployment validation.

## Constraints
Do not modify active homelab or XPS pilots as part of architectural approval. The project must remain independent of machine names and provider brands. Avoid false claims of official vendor association or universal provider compatibility.

## Decisions
See ADR-001 through ADR-005; contract revision 1.
