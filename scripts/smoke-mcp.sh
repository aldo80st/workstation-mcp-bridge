#!/bin/sh
set -eu
url="${MCP_URL:-http://127.0.0.1:8765/mcp}"
echo "MCP initialize: $url"
curl -fsS -i -m 15 -X POST "$url" \
 -H 'Accept: application/json, text/event-stream' \
 -H 'Content-Type: application/json' \
 -H 'MCP-Protocol-Version: 2025-03-26' \
 --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"wmb-smoke","version":"0.1.0"}}}'
