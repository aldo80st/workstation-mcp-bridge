# Getting started

Requires Docker Engine and Compose with `up --wait`, Linux ARM64 or AMD64, and daemon access. Verify `docker version`, `docker compose version`, free disk/RAM, `docker ps -a` and the chosen port before installation. Never stop an existing service to free a port without authorization.

Clone this repository into a new directory. Create `workspace` explicitly; Compose refuses missing bind sources. Copy `.env.example` to `.env`, set `MCP_HOST_PORT` to a free loopback port and match `MCP_UID`/`MCP_GID` to `id -u`/`id -g`. Use disposable fixtures for initial validation.

```sh
mkdir -p workspace
printf 'MCP_SMOKE_FIXTURE\n' > workspace/README.txt
docker compose config --quiet
docker compose build
docker compose up -d --wait --wait-timeout 90
curl -fsS http://127.0.0.1:8765/healthz
MCP_URL=http://127.0.0.1:8765/mcp ./scripts/smoke-mcp.sh
```

Substitute your configured host port/path in client commands. Health initializes and pings the MCP child; the response is cached for up to ten seconds. No npm downloads occur during startup. Image base digest and dependency integrity are pinned; upgrades require editing the lockfile, rebuilding and rerunning both architectures.
