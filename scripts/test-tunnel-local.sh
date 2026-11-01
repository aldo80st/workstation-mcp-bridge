#!/bin/sh
# No OpenAI traffic: synthetic key/ID, local MCP backend also answers control-plane attempts.
set -eu
cd "$(dirname "$0")/.."
project="${WMB_TEST_PROJECT:-workstation-mcp-bridge}"
name="wmb-tunnel-test-$$"
mkdir -p .evidence
key=$(mktemp "$PWD/.evidence/tunnel-key.XXXXXX")
log=$(mktemp "$PWD/.evidence/tunnel-log.XXXXXX")
# shellcheck disable=SC2329 # Invoked indirectly by EXIT/INT/TERM traps.
cleanup() {
    status=$?
    trap - EXIT INT TERM
    docker stop "$name" >/dev/null 2>&1 || true
    docker rm "$name" >/dev/null 2>&1 || true
    rm -f "$key"
    exit "$status"
}
trap 'cleanup' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf 'synthetic-unused-key-for-validation\n' > "$key"
chmod 600 "$key"
MCP_UID=$(id -u)
MCP_GID=$(id -g)
export MCP_UID MCP_GID
export CONTROL_PLANE_TUNNEL_ID=tunnel_0123456789abcdef0123456789abcdef
export CONTROL_PLANE_API_KEY_FILE="$key"
backend="http://workstation-mcp:${MCP_PORT:-8765}"
docker compose -p "$project" -f compose.yaml -f compose.tunnel.yaml --profile tunnel \
    run -d --name "$name" --no-deps tunnel-client run \
    --control-plane.api-key=file:/run/secrets/control-plane-api-key \
    --control-plane.base-url="$backend" --mcp.startup-wait-timeout=10s >/dev/null
for attempt in $(seq 1 30); do
    docker logs "$name" > "$log" 2>&1
    if grep -q 'permission denied' "$log" || grep -q 'synthetic-unused-key-for-validation' "$log"; then
        echo 'Tunnel secret loading/redaction failed' >&2
        exit 1
    fi
    if grep -q 'mcp session initialized' "$log" && grep -q 'poll failed; backing off' "$log"; then
        printf 'Tunnel secret loading, MCP discovery and local control-plane retry verified\n'
        exit 0
    fi
    sleep 1
done
echo "Tunnel did not reach expected local probe state after $attempt attempts; inspect $log" >&2
exit 1
