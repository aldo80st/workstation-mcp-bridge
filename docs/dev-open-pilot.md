# Reboot recovery and Open sidecar pilot (operator runbook)

Status: pilot only. No stable release and no assumption that a healthy container
equals a working ChatGPT connection.

If readiness reports `startup catalog failed`, recover and validate Restricted
first using [the version-specific recovery procedure](tunnel-startup-recovery.md).
The tunnel overlay includes a bounded MCP startup wait for Docker restarts.

## Topology and scope

Existing Compose project: `wmb-pilot`. Its `workstation-mcp` (Restricted)
is the read-only fallback; `workstation-mcp-open` is a separate Open instance
with an explicitly selected Git checkout mounted read-write. The
`tunnel-client` can route to either instance. Reuse the *existing* tunnel
identity and secret file; do not issue or copy credentials. A separate,
canonical Ánima XPS tunnel may also exist: inspect rather than confuse them.
This procedure changes only `wmb-pilot`, not other gateways or devices.

The Open container has no host-published port, no Docker socket mount,
no privileged mode and no entire-home/root mount. The Open profile can
execute processes and make network requests *inside its container*; it is
not a security sandbox for untrusted arbitrary code.

## 1. Inspect after a host reboot (read-only)

```bash
docker ps --filter 'label=com.docker.compose.project=wmb-pilot' \
  --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker inspect wmb-pilot-tunnel-client-1 \
  --format '{{.State.Status}}'
docker inspect wmb-pilot-tunnel-client-1 \
  --format '{{range .Config.Env}}{{println .}}{{end}}' |
  grep '^MCP_SERVER_URL='
```

Expected: Restricted healthy, Open healthy if previously enabled,
tunnel-client running, and a backend URL that is either
`http://workstation-mcp:8765/mcp` (Restricted) or
`http://workstation-mcp-open:8765/mcp` (Open). A host restart invalidates
some remote MCP sessions even when containers are restarted automatically.
Do not print a full environment dump or tunnel logs containing credentials.

## 2. Restore Open locally without recreating credentials

Only on explicit user authorization; use a trusted existing Git checkout
inside the home directory. Export values again after reboot or use
per-command variables. Run Compose from this checkout and keep both
`compose.tunnel.yaml` and `compose.dev-open.yaml` in the same project:

```bash
cd ~/labs/workstation-mcp-bridge
export MCP_DEV_WORKSPACE_PATH="/absolute/path/to/authorized/git-checkout"
export MCP_OPEN_ACK="I_ACCEPT_OPEN_MODE_RISKS"
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  -f compose.dev-open.yaml --profile developer --profile tunnel \
  config --quiet
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  -f compose.dev-open.yaml --profile developer --profile tunnel \
  up -d --no-build --no-deps workstation-mcp-open
```

Check `workstation-mcp-open` health and the actual MCP `tools/list`:
`start_process`, `write_file`, and `read_file` must be discoverable.
Do not redirect a tunnel merely because the health endpoint returned 200.

## 3. Switch the existing pilot tunnel only after validation

The following command recreates only the tunnel client in the selected
project and can cause a brief disconnection. It does not change the
canonical Ánima tunnel if that is a different deployment.

```bash
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  -f compose.dev-open.yaml --profile developer --profile tunnel \
  up -d --no-build --no-deps --force-recreate tunnel-client
```

Verify the tunnel container is running, its *non-secret backend URL*
points to `workstation-mcp-open`, and ChatGPT can invoke a read-only
fixture call. Note: ChatGPT connector schemas can remain frozen at the
original Restricted tool list; updating server-side tools does not
automatically refresh an installed ChatGPT connector.

## 4. Restricted rollback (no data deletion)

To switch only this pilot tunnel back to Restricted, omit the Open
overlay and explicitly keep the default backend (if no local
`MCP_SERVER_URL` override was previously set):

```bash
unset MCP_SERVER_URL
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  --profile tunnel up -d --no-build --no-deps --force-recreate tunnel-client
```

Confirm `MCP_SERVER_URL=http://workstation-mcp:8765/mcp`, check Restricted
health and a fixture read. Do not tear down the whole Compose project, prune Docker resources, or
restart Docker system-wide as part of this drill.

## Pilot acceptance gates

1. Post-reboot containers running, health and backend URL verified.
2. Local Open `initialize`, `tools/list`, and (only in disposable CI)
   write/command smoke pass.
3. Authenticated tunnel routes to expected service after restart.
4. ChatGPT reconnection and tool discovery verified independently.
5. Restricted rollback restores reads while blocking writes.
6. No credential exposure, no host-wide Docker disruption.

Treat any unobserved gate as PENDING; one cannot infer end-to-end tunnel
recovery from local `tools/list` alone.
