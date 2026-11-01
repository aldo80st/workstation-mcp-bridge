# Operations

For post-reboot `startup catalog failed` on tunnel-client v0.0.19, see
[tunnel startup recovery](tunnel-startup-recovery.md). Recover Restricted before
considering the optional Open route.

Use an explicit Compose project name to isolate pilots, for example `docker compose -p wmb-pilot ...`. Keep its checkout, `.env`, workspace and secrets independent of earlier deployments. `docker compose ps` and `/healthz` show runtime health; inspect bounded logs with `docker compose logs --tail 80 workstation-mcp`. Tool logs may contain paths or file content; keep diagnostics private.

Container restart: `docker compose restart workstation-mcp`, then `docker compose up -d --wait --wait-timeout 90`. Configuration changes require `up -d`, not just restart. Both services use `restart: unless-stopped`; manually stopped services stay stopped after a daemon restart. A Docker daemon restart affects every local container and must be scheduled separately if other services are running. Container stop/start testing does not prove a real daemon restart.

Before updates, record commit and `docker image inspect workstation-mcp-bridge:local`, preserve `.env` and protected secrets locally, and tag the known image with a project-specific rollback tag. Build the new image and run `scripts/validate-local.sh` with an isolated project before updating the pilot. Do not run a host-wide prune.

Rollback: check out the recorded commit in a separate clean directory, restore only that deployment's settings, select the previously recorded image/tag, and recreate only that Compose project. Re-run health and direct read/deny tests. Workspaces are bind mounts; `down` does not delete their data. Do not use `down -v` or delete data to roll back.

Local regression harness uses `.evidence` workspaces and leaves its runtime in Restricted: `WMB_TEST_PROJECT=wmb-validation MCP_HOST_PORT=18795 scripts/validate-local.sh`. Do not point it at a production project. Full Docker daemon restart and host reboot remain separate acceptance checks.
