# Security profiles

Restricted uses a read-only bind at `/workspace`, non-root UID/GID, dropped capabilities, no-new-privileges, process/memory/CPU limits and loopback publication. Supergateway 4.2.1 `--tools` denies forbidden direct calls, not only discovery. Desktop Commander starts with `allowedDirectories: ["/workspace"]`; canonical path checks reject traversal and symlinks outside it. Startup resets this configuration and disables telemetry.

Allowed tools: read_file, read_multiple_files, list_directory; directory_tree is requested only if upstream exposes it. Read-file URL functionality is upstream functionality and is not an egress firewall. The bridge network currently permits outbound traffic. Do not describe Restricted as a network sandbox; do not put untrusted network services on its bridge.

Open requires both settings and the override:

```sh
mkdir -p test-open
export MCP_OPEN_WORKSPACE_PATH="$PWD/test-open"
export MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS
docker compose -f compose.yaml -f compose.open.yaml up -d --wait --wait-timeout 90
```

**Warning:** Open permits commands and file modification as the container user. Commands can bypass the application's directory policy, access container files and network, and modify any writable mount. Host isolation depends on the mounts and Docker security boundary. Never use sensitive directories for smoke tests.

Return to Restricted with `docker compose up -d --wait --wait-timeout 90` (omit the Open override). This recreates the runtime, restores a read-only mount and resets application policy; it does not delete the Open workspace. Re-run direct forbidden calls. An unchanged container merely restarted retains its previous profile.

Local loopback is not application authentication: other local processes may connect. Remote transport must be authenticated. No real credentials belong in the tool container; tunnel secrets belong only in the optional adapter.
