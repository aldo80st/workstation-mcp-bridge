# Troubleshooting

- Docker permission denied: verify your account's daemon permission. Daemon access grants host-level control; never change socket permissions to 0666. A temporary ACL may be lost when Docker recreates its socket.
- Docker buildx lock permission denied: set `DOCKER_CONFIG` to a new empty directory inside the project. Do not overwrite another installation's Docker configuration.
- Port occupied: choose another MCP_HOST_PORT; leave the existing listener running.
- Missing workspace: create the intended path explicitly and check ownership. Bind mounts intentionally do not auto-create host paths.
- Unhealthy: inspect logs; health checks MCP initialization/ping, caches for ten seconds and may take ten seconds to fail. Check memory/process limits, command availability and workspace permissions.
- Restricted read denied: use paths inside `/workspace`; symlinks outside are deliberately rejected.
- Open refused: set the explicit workspace and exact acknowledgement. Stop/recreate with the correct Compose overlays.
- Tunnel key permission denied: align MCP_UID/GID with the owner of the mode-0600 key. Do not print the key or weaken it to world-readable.
- Tunnel exits or stays unready: verify the ID, key permissions, authorized account/workspace, outbound HTTPS and internal MCP URL. Startup with dummy credentials is not an external connectivity test.
- MCP protocol errors: use JSON-RPC and Accept `application/json, text/event-stream`; the tested baseline uses protocol 2025-03-26. A health response alone does not prove tool authorization.
