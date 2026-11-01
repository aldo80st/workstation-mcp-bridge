#!/bin/sh
set -eu
profile="${MCP_SECURITY_PROFILE:-restricted}"
port="${MCP_PORT:-8765}"
path="${MCP_PATH:-/mcp}"
case "$port" in ''|*[!0-9]*) echo "Invalid MCP_PORT" >&2; exit 64;; esac
[ "$port" -ge 1024 ] && [ "$port" -le 65535 ] || { echo "Port outside unprivileged range" >&2; exit 64; }
case "$path" in /*) ;; *) echo "MCP_PATH must start with /" >&2; exit 64;; esac
case "$path" in *[!a-zA-Z0-9/_.-]*|*'..'*|/healthz|/) echo "Invalid MCP_PATH" >&2; exit 64;; esac
# Express ignores route case and trailing slashes; URL clients normalize dot segments.
case "$path/" in */./*) echo "Invalid MCP_PATH dot segment" >&2; exit 64;; esac
normalized_path=$(printf '%s' "$path" | tr '[:upper:]' '[:lower:]' | sed 's:/*$::')
[ "$normalized_path" != /healthz ] || { echo "MCP_PATH conflicts with health route" >&2; exit 64; }
[ -d /workspace ] || { echo "Missing workspace" >&2; exit 64; }
set -- --stdio "desktop-commander --no-onboarding" \
  --outputTransport streamableHttp --port "$port" --host 0.0.0.0 \
  --streamableHttpPath "$path" --healthEndpoint /healthz --healthCheck server --logLevel info
case "$profile" in
  restricted)
    # In Supergateway these are an actual tools/call allowlist, not merely tools/list filtering.
    set -- "$@" --tools read_file --tools read_multiple_files --tools list_directory --tools directory_tree
    ;;
  open)
    if [ "${MCP_OPEN_ACK:-}" != "I_ACCEPT_OPEN_MODE_RISKS" ]; then
      echo "Open mode requires MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS" >&2
      exit 64
    fi
    echo "WARNING: OPEN MODE permits command execution and filesystem modification within mounts." >&2
    ;;
  *) echo "Unknown MCP_SECURITY_PROFILE" >&2; exit 64 ;;
esac
if [ -n "${MCP_API_KEY_FILE:-}" ]; then
  [ -s "$MCP_API_KEY_FILE" ] || { echo "Missing MCP API key file" >&2; exit 64; }
  set -- "$@" --apiKeyFile "$MCP_API_KEY_FILE"
fi
node /usr/local/lib/wmb/configure.mjs
exec supergateway "$@"
