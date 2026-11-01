# Tunnel startup recovery (v0.0.19)

Status: local ARM64 recovery verified; independent ChatGPT acceptance pending.
Keep the Open pilot PR in draft until its acceptance gates are met.

## Cause and minimal correction

After the XPS restart, Docker started the backend and tunnel client concurrently.
At `2026-11-01T04:24:02Z`, the client resolved `workstation-mcp` but received
`ECONNREFUSED` from port 8765 during MCP initialize and discovery. The backend
subsequently became healthy. The client stayed running with `/healthz` 200,
`/readyz` 503 (`startup catalog failed`), and no successful control-plane polls.
Fetching tunnel metadata succeeded: this was not evidence of an invalid key.

The installed binary is `0.0.19+01d67bb4da0d8359b808b4761f8db171ab682cd7`.
In that exact revision:

- [`pkg/oauth/module.go`](https://github.com/openai/tunnel-client/blob/01d67bb4da0d8359b808b4761f8db171ab682cd7/pkg/oauth/module.go#L193)
  waits for MCP only when startup wait is enabled. A non-optional discovery
  failure completes the startup catalog with an error. The presence of this
  discovery module does not mean the backend requires OAuth.
- [`pkg/controlplane/fx/fxmodule.go`](https://github.com/openai/tunnel-client/blob/01d67bb4da0d8359b808b4761f8db171ab682cd7/pkg/controlplane/fx/fxmodule.go#L378)
  disables polling when that catalog fails; its readiness gate reports the
  exact `startup catalog failed` message.
- [`pkg/mcpclient/fxmodule.go`](https://github.com/openai/tunnel-client/blob/01d67bb4da0d8359b808b4761f8db171ab682cd7/pkg/mcpclient/fxmodule.go#L196)
  enables bounded initialize retries, including connection refused, when
  `MCP_STARTUP_WAIT_TIMEOUT` is positive.

`compose.tunnel.yaml` now sets `MCP_STARTUP_WAIT_TIMEOUT: "120s"`. This uses
the installed client's existing recovery path and delays OAuth discovery as
well as polling until the MCP startup probe completes. Compose's
`depends_on: service_healthy` remains useful for `compose up`; Docker's restart
manager does not replay that Compose ordering on host boot.

No image rebuild, version upgrade, new tunnel, new key, public listener, or
profile change is needed. The wait is bounded: an unavailable backend beyond
120 seconds still requires operator diagnosis. A client healthcheck alone
would report the failure without repairing it.

## Diagnose without disclosing credentials

Use the intended Compose project and inspect its labels first. A separate
`anima-xps-tunnel-direct` deployment may coexist; do not restart or reconfigure
it as part of this procedure. Do not dump `.env`, all container environment
variables, or unredacted logs.

```sh
docker exec wmb-pilot-tunnel-client-1 tunnel-client health \
  --port 8080 --json --require-control-plane-poll
docker exec wmb-pilot-tunnel-client-1 wget -qO- \
  'http://127.0.0.1:8080/health?details=true'
docker exec wmb-pilot-tunnel-client-1 wget -qO- \
  http://127.0.0.1:8080/health/mcp
docker exec wmb-pilot-tunnel-client-1 wget -qO- \
  http://127.0.0.1:8080/health/control-plane
docker exec wmb-pilot-tunnel-client-1 wget -qO- \
  http://workstation-mcp:8765/healthz
```

Expected healthy output: both health endpoints 200 and a successful
control-plane poll. The first long poll may take 30 seconds to complete;
readiness alone does not establish successful polling. Per-component health
endpoints can return HTTP 200 while the component JSON reports a failure.
For this HTTP transport, `/health/mcp` can report `same_child_evidence_unavailable`;
verify initialize and tools directly instead of interpreting that as success.

## Apply and reverse

Record the image digest, non-secret backend URL, restart policy, mounts,
Compose file list, and the previous `compose.tunnel.yaml` before intervention.
Keep backups local. Preserve the existing `.env` and secret file in place.

First confirm Restricted accepts initialize, tools/list, and a known workspace
read. For a stuck catalog with an already healthy backend, restarting only
`wmb-pilot-tunnel-client-1` restores discovery. To persist the startup-wait
correction, run from the existing deployment checkout:

```sh
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  --profile tunnel config --quiet
docker compose -p wmb-pilot -f compose.yaml -f compose.tunnel.yaml \
  --profile tunnel up -d --no-build --no-deps --force-recreate tunnel-client
```

Preflight the effective backend privately. If `.env` sets `MCP_SERVER_URL`,
it must still resolve to the intended Restricted service for this recovery.
Omit `compose.dev-open.yaml` during the initial repair. Confirm the image,
tunnel identity and secret source are unchanged, without printing them.

To reverse this correction, restore the recorded `compose.tunnel.yaml` and
repeat the same command to recreate **only** `tunnel-client`. Keep the backend
healthy before reversing; the original boot race returns without startup wait.
Do not tear down the project or restart Docker. Configuration rollback was
exercised by rendering the recorded prior Compose configuration; reintroducing
the defective configuration into the live client is not an acceptance test.

## Acceptance and observed evidence

- Before correction: health probe exited 2 with healthz 200, readyz 503 and no
  successful poll; direct MCP from the same tunnel container succeeded.
- Restricted: all 11 existing MCP integration tests passed, including workspace
  read, hidden write/process tools, direct denied calls, traversal and outside
  workspace rejection.
- Compose regression: RED before the setting existed; GREEN after the change.
  All 14 unit/configuration tests passed on ARM64.
- Existing Open sidecar: single explicit checkout mount, no host root/home or
  Docker socket, no published host port, non-root user and dropped capabilities.
  Local initialize, 25 tools, container `pwd`, and temporary write/read were
  tested. The unique temporary file was removed. Tunnel remains Restricted.
- An actual connected-tool read succeeded from Codex after recovery. This is
  separate from ChatGPT product acceptance.

Repeat the health/poll check after an isolated restart of the affected client.
The exact race was observed in the host restart logs; a new full host/daemon
restart and a synthetic delayed-backend drill were not performed in this session.
The existing dual-architecture CI must pass on the final PR head before claiming
AMD64 runtime verification.

Classify the result as `LOCAL_VERIFIED / CHATGPT_E2E_PENDING` until a real
ChatGPT read of the known fixture succeeds. Refresh or renew the existing
ChatGPT connection only if that independent call still fails after local
readiness and polling recover. Do not create another tunnel identity.

For an optional Open route, follow [the reversible pilot runbook](dev-open-pilot.md).
Prevalidate Open locally, retain the same tunnel identity and secret, and keep
the Restricted Compose command above as the return path. No route switch is
part of this initial repair.
