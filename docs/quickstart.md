# Quickstart (experimental / unverified outside tested platforms)

## Prerequisites
Docker Engine with Compose v2; Linux ARM64 or AMD64, free localhost port 8765.

## Restricted (default)

```sh
git clone https://github.com/aldo80st/workstation-mcp-bridge.git
cd workstation-mcp-bridge
git switch feat/usable-containers-v0.1  # pilot branch until PR #19 is merged
cp .env.example .env
mkdir -p workspace secrets
docker compose build
docker compose up -d
docker compose ps
sh scripts/smoke-mcp.sh
```

Restricted intentionally exposes only Supergateway-allowlisted read-only tools, and mounts `./workspace` read-only. Test the `tools/call` deny before trusting restricted in your environment. Docker namespace boundaries do **not** guarantee sandboxing from network attacks, exfiltration of readable files, or vulnerabilities in upstream components. The public port is loopback-only.

## Open (opt-in)

**DANGER:** AI tools can execute arbitrary commands, rewrite files, or delete content within authorized mounts; prompt injection may cause unintended actions.

Edit `.env` with `MCP_OPEN_WORKSPACE_PATH=/absolute/path/to/disposable/test-workspace` and `MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS`. Then:

```sh
docker compose -f compose.yaml -f compose.open.yaml config --quiet
docker compose -f compose.yaml -f compose.open.yaml up -d --build
```

To return to Restricted: `docker compose -f compose.yaml -f compose.open.yaml down` then `docker compose up -d`. Do not use Open on production folders.

## Secure MCP Tunnel (optional second container)

Configure `CONTROL_PLANE_TUNNEL_ID` in `.env`; create `secrets/control-plane-api-key` and protect it with `chmod 600`. Never commit the key. Start:

```sh
docker compose -f compose.yaml -f compose.tunnel.yaml --profile tunnel config --quiet
docker compose -f compose.yaml -f compose.tunnel.yaml --profile tunnel up -d --build
docker compose -f compose.yaml -f compose.tunnel.yaml --profile tunnel ps
```

Tunnel-client is for OpenAI-hosted clients, not universal MCP connectivity. Use actual platform-generated Tunnel ID and runtime API key. Local mode works without it. Verify tunnel-client supported image tag/arch and permissions before real credentials. The MCP server is reachable by the tunnel container on a private Docker network. No TCP port is opened beyond localhost.

## Troubleshooting

- Inspect: `docker compose ps` / `docker compose logs --tail=80 workstation-mcp`.
- If 8765 is taken, set `MCP_HOST_PORT=18765`, `MCP_URL=http://127.0.0.1:18765/mcp`.
- If Docker cannot mount `workspace`, use an absolute existing directory in `.env`.
- This repository is unaffiliated with upstream projects; see ADRs and planned license review #4.
