# Providers and optional Secure MCP Tunnel

Local clients use Streamable HTTP at `http://127.0.0.1:8765/mcp` (adjust port/path). The local baseline works without a vendor adapter. Only tested clients/transports belong in the compatibility matrix.

Tunnel client v0.0.19 is pinned by multi-platform digest. Its real `run --help` confirms `CONTROL_PLANE_TUNNEL_ID`, `MCP_SERVER_URL` and `--control-plane.api-key=file:/path`. Supply a real ID and a mode-0600 key file, owned by MCP_UID. Compose local secrets are bind mounts; file ownership matters, and a mode-0600 file owned by a different UID fails to open. Never chmod secrets world-readable.

```dotenv
CONTROL_PLANE_TUNNEL_ID=tunnel_REPLACE_WITH_REAL_ID
CONTROL_PLANE_API_KEY_FILE=./secrets/control-plane-api-key
MCP_SERVER_URL=http://workstation-mcp:8765/mcp
```

```sh
chmod 600 secrets/control-plane-api-key
docker compose -f compose.yaml -f compose.tunnel.yaml --profile tunnel config --quiet
docker compose -f compose.yaml -f compose.tunnel.yaml --profile tunnel up -d --wait --wait-timeout 90
```

Do not paste keys in commands, chat or committed files. Existing credentials from other installations are not reused automatically. The adapter makes outbound HTTPS connections and publishes no host port. Restart policy is unless-stopped; inspect readiness and logs before claiming connectivity. Missing/invalid credentials do not constitute a working tunnel.

For ChatGPT, create or select an authorized tunnel in Platform tunnel settings, associate the intended ChatGPT workspace and grant the operator Tunnels Read + Use. In ChatGPT Plugins, add a custom MCP server, choose Connection: Tunnel and select that ID. Complete discovery and a safe read call. This integration remains unverified until that call succeeds with authorized credentials.

Source: [official OpenAI Secure MCP Tunnel documentation](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels). Account availability and workspace permissions must be checked in the target account. Synthetic credential tests only verify local configuration, startup/error handling and backend discovery.
