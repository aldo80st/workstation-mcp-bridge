#!/bin/sh
# Only touches this script's explicit Compose project and synthetic fixtures.
set -eu
cd "$(dirname "$0")/.."
project="${WMB_TEST_PROJECT:-wmb-validation}"
export MCP_HOST_PORT="${MCP_HOST_PORT:-18795}"
export MCP_URL="http://127.0.0.1:${MCP_HOST_PORT}${MCP_PATH:-/mcp}"
export MCP_WORKSPACE_PATH="$PWD/.evidence/restricted-workspace"
export MCP_OPEN_WORKSPACE_PATH="$PWD/.evidence/open-workspace"
mkdir -p "$MCP_WORKSPACE_PATH" "$MCP_OPEN_WORKSPACE_PATH"
printf 'MCP_SMOKE_FIXTURE\n' > "$MCP_WORKSPACE_PATH/README.txt"
ln -sf /etc/passwd "$MCP_WORKSPACE_PATH/outside-link"
compose() { docker compose -p "$project" "$@"; }
compose up -d --no-build --wait --wait-timeout 90
python3 -m unittest discover -s tests/integration -p test_mcp.py -v
python3 -m unittest discover -s tests/integration -p test_startup.py -v
compose restart workstation-mcp
compose up -d --no-build --wait --wait-timeout 90
python3 -m unittest discover -s tests/integration -p test_mcp.py -v
compose stop workstation-mcp
compose up -d --no-build --wait --wait-timeout 90
python3 -m unittest discover -s tests/integration -p test_mcp.py -v
open_active=false
cleanup() {
    status=$?
    trap - EXIT INT TERM
    if [ "$open_active" = true ]; then
        if ! compose up -d --no-build --wait --wait-timeout 90; then
            compose stop workstation-mcp || true
        fi
    fi
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
open_active=true
export MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS
compose -f compose.yaml -f compose.open.yaml up -d --no-build --wait --wait-timeout 90
python3 -m unittest discover -s tests/integration -p test_open.py -v
grep -q OPEN_SMOKE_OK "$MCP_OPEN_WORKSPACE_PATH/allowed.txt"
grep -q WMB_OPEN_COMMAND_OK "$MCP_OPEN_WORKSPACE_PATH/command.txt"
# Dropping the override must recreate the read-only default.
compose up -d --no-build --wait --wait-timeout 90
open_active=false
python3 -m unittest discover -s tests/integration -p test_mcp.py -v
grep -q OPEN_SMOKE_OK "$MCP_OPEN_WORKSPACE_PATH/allowed.txt"
test ! -e "$MCP_WORKSPACE_PATH/forbidden.txt"
test ! -e "$MCP_WORKSPACE_PATH/prohibited-command-marker"
