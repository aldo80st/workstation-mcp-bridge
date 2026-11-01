# Workstation MCP Bridge

**Status: Architecture approved · v0.1 · not yet an operational release.**

A provider-neutral, containerized integration of the open-source Desktop Commander MCP server with Supergateway. Optional connection adapters (including OpenAI Secure MCP Tunnel) are planned, not yet implemented.

## Security profiles

- **Restricted** (default): explicit workspace mounts and enforceable MCP call restrictions. Tool visibility alone is not an access-control boundary.
- **Open** (opt-in): broader user-authorized access **only after a prominent security warning**. Open does **not** mean public or unauthenticated Internet access.

**Security warning:** MCP tools may read/write files and execute commands within authorized scopes. AI automation and prompt-injection attacks can cause accidental data loss or unauthorized actions. Never publish an unauthenticated endpoint, mount host root or Docker socket by default, or commit secrets.

## Current documentation

- [Project context](.ai-architect/project-context.md)
- [Architecture contract](.ai-architect/architecture-contract.yaml)
- [Implementation plan](.ai-architect/implementation-plan.md)
- [Architectural decisions](.ai-architect/decisions/)

No container is deployed from this repository yet. Supported platform/provider combinations will be listed only after verification.

## Independence and attribution

This project is independent and is not affiliated with, endorsed by, or an official version of Desktop Commander or any AI service provider. It will reuse third-party software only under the applicable licenses and notices; final distribution and trademark checks are pending.
