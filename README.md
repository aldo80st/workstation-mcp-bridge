# Workstation MCP Bridge

A provider-neutral Desktop Commander OSS + Supergateway runtime for local MCP Streamable HTTP. Optional Secure MCP Tunnel runs in a separate container. Pilot only; stable release remains blocked by security findings and distribution review.

Restricted is the default: read-only workspace, explicit read-tool allowlist enforced on direct calls, and workspace path policy. Open requires an explicit workspace and acknowledgement; it enables command execution and writes under container permissions.

```sh
mkdir -p workspace
printf 'MCP_SMOKE_FIXTURE\n' > workspace/README.txt
cp .env.example .env
# Choose a free MCP_HOST_PORT; use 18795 if 8765 is occupied.
docker compose up -d --build --wait --wait-timeout 90
./scripts/smoke-mcp.sh
```

Do not expose unauthenticated MCP to the Internet or mount host root/home or Docker socket. Open commands can access the container filesystem and network, beyond the mounted workspace. Desktop Commander path settings complement container isolation; they are not a host sandbox.

See [getting started](docs/getting-started.md), [security profiles](docs/security-profiles.md), [providers](docs/providers.md), [operations](docs/operations.md), [troubleshooting](docs/troubleshooting.md), [compatibility](docs/compatibility-matrix.md), [security status](docs/security-findings.md), and [release gates](docs/release-checklist.md).

## Architecture and attribution

Accepted [ADRs](.ai-architect/decisions/) and [architecture contract](.ai-architect/architecture-contract.yaml) govern implementation. Independent project, not affiliated with or endorsed by Desktop Commander, Supergateway or OpenAI. See [NOTICE](NOTICE.md). No stable image or release is published by these instructions.
