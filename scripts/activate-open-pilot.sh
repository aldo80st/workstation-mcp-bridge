#!/usr/bin/env bash
# Existing WMB tunnel: opt-in route from Restricted to already-running Open.
# Usage: cd ~/labs/workstation-mcp-bridge && bash scripts/activate-open-pilot.sh
set -Eeuo pipefail

project=wmb-pilot
open=wmb-pilot-workstation-mcp-open-1
restricted=wmb-pilot-workstation-mcp-1
tunnel=wmb-pilot-tunnel-client-1
old_url=http://workstation-mcp:8765/mcp
new_url=http://workstation-mcp-open:8765/mcp

for file in compose.yaml compose.tunnel.yaml compose.dev-open.yaml; do
  [[ -f "$file" ]] || { echo "Missing $file: run inside the WMB checkout" >&2; exit 2; }
done
command -v docker >/dev/null || { echo 'Docker CLI missing' >&2; exit 2; }
[[ "$(docker inspect --format '{{.State.Health.Status}}' "$restricted")" == healthy ]] || {
  echo "Restricted is unhealthy; switch refused" >&2; exit 2;
}
[[ "$(docker inspect --format '{{.State.Health.Status}}' "$open")" == healthy ]] || {
  echo "Open is unhealthy; switch refused" >&2; exit 2;
}

current_url=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$tunnel" | sed -n 's/^MCP_SERVER_URL=//p')
if [[ "$current_url" == "$new_url" ]]; then
  echo "Open already selected by this pilot; no change"
  exit 0
fi
[[ "$current_url" == "$old_url" ]] || {
  echo "Unrecognized tunnel destination; switch refused" >&2; exit 2;
}

# Reuse the EXACT mounted workspace. Do not mount host root, HOME or Docker.
export MCP_DEV_WORKSPACE_PATH="$(docker inspect --format '{{range .Mounts}}{{if eq .Destination "/workspace"}}{{.Source}}{{end}}{{end}}' "$open")"
[[ -d "$MCP_DEV_WORKSPACE_PATH" && -e "$MCP_DEV_WORKSPACE_PATH/.git" ]] || {
  echo "Open workspace must be an existing Git checkout" >&2; exit 2;
}
[[ "$(realpath "$MCP_DEV_WORKSPACE_PATH")" != "/" && "$(realpath "$MCP_DEV_WORKSPACE_PATH")" != "$(realpath "$HOME")" ]] || {
  echo "Whole host HOME/root mount forbidden" >&2; exit 2;
}
docker inspect "$open" | python3 -c '
import json,sys
c=json.load(sys.stdin)[0]; m=c["Mounts"]; env=c["Config"]["Env"]
assert len(m)==1 and m[0]["Destination"]=="/workspace" and m[0]["RW"] is True
assert "/var/run/docker.sock" not in str(m)
assert not c["HostConfig"].get("Privileged")
assert "ALL" in (c["HostConfig"].get("CapDrop") or [])
assert not c["NetworkSettings"]["Ports"].get("8765/tcp")
assert "MCP_SECURITY_PROFILE=open" in env
assert "MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS" in env
print("Open container isolation: PASS")
'

export MCP_OPEN_ACK=I_ACCEPT_OPEN_MODE_RISKS
docker compose -p "$project" -f compose.yaml -f compose.tunnel.yaml -f compose.dev-open.yaml \
  --profile tunnel --profile developer config --quiet

# A Compose re-create must NOT silently change the tunnel ID, image or key file.
live_id=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$tunnel" | sed -n 's/^CONTROL_PLANE_TUNNEL_ID=//p')
live_image=$(docker inspect --format '{{.Config.Image}}' "$tunnel")
live_secret=$(docker inspect --format '{{range .Mounts}}{{if eq .Destination "/run/secrets/control-plane-api-key"}}{{.Source}}{{end}}{{end}}' "$tunnel")
[[ -n "$live_id" && -n "$live_secret" ]] || { echo 'Tunnel identity/secret missing' >&2; exit 2; }

config_json=$(docker compose -p "$project" -f compose.yaml -f compose.tunnel.yaml -f compose.dev-open.yaml \
  --profile tunnel --profile developer config --format json)
IFS=$'\t' read -r next_id next_image next_secret next_url < <(
  printf '%s' "$config_json" | python3 -c '
import json,sys
x=json.load(sys.stdin); t=x["services"]["tunnel-client"]
print("\t".join([t["environment"]["CONTROL_PLANE_TUNNEL_ID"],t["image"],
                 x["secrets"]["control-plane-api-key"]["file"],
                 t["environment"]["MCP_SERVER_URL"]]))
')
[[ "$live_id" == "$next_id" && "$live_image" == "$next_image" && "$next_url" == "$new_url" ]] || {
  echo 'Tunnel ID, image or destination mismatch; switch refused' >&2; exit 2;
}
[[ "$(realpath "$live_secret")" == "$(realpath "$next_secret")" ]] || {
  echo 'Existing tunnel credential file differs from rendered Compose' >&2; exit 2;
}

# Check real MCP discovery before changing the tunnel; do not run a command/write.
docker exec -i "$open" node - <<'JS'
const url = 'http://127.0.0.1:8765/mcp';
async function rpc(method,id,params={}) {
  const res=await fetch(url,{
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Accept':'application/json, text/event-stream',
      'MCP-Protocol-Version':'2025-03-26'
    },
    body:JSON.stringify({jsonrpc:'2.0',id,method,params})
  });
  if(!res.ok) throw Error('MCP '+method+' HTTP '+res.status);
  const data=await res.text();
  const payload=data.trim().startsWith('{')
      ? data.trim()
      : data.split(/\r?\n/).filter(line=>line.startsWith('data:')).map(line=>line.slice(5).trim()).at(-1);
  if(!payload) throw Error('No JSON-RPC payload for '+method);
  const parsed=JSON.parse(payload);
  if(parsed.error) throw Error('MCP error from '+method);
  return parsed.result;
}
(async()=>{
  const init=await rpc('initialize',1,{protocolVersion:'2025-03-26',capabilities:{},
    clientInfo:{name:'wmb-open-pilot',version:'0.1'}});
  if(!init?.serverInfo) throw Error('MCP initialize missing serverInfo');
  const list=await rpc('tools/list',2);
  const names=new Set((list?.tools??[]).map(t=>t.name));
  for(const name of ['read_file','write_file','start_process']){
    if(!names.has(name)) throw Error('Open tool not found: '+name);
  }
  console.log('Open MCP tool discovery PASS: '+names.size+' tools');
})().catch(e=>{console.error(e.message);process.exit(1)});
JS

rollback_armed=0
rollback() {
  code=$?
  trap - EXIT
  if [[ "$rollback_armed" -eq 1 && "$code" -ne 0 ]]; then
    echo 'Open switch failed; attempting Restricted rollback' >&2
    if MCP_SERVER_URL=http://workstation-mcp:8765/mcp docker compose -p "$project" \
      -f compose.yaml -f compose.tunnel.yaml --profile tunnel \
      up -d --no-build --no-deps --force-recreate tunnel-client; then
      echo 'Restricted rollback attempted; verify tunnel health' >&2
    else
      echo 'ALERT: automatic rollback failed; manual intervention required' >&2
    fi
  fi
  exit "$code"
}
trap rollback EXIT
rollback_armed=1
docker compose -p "$project" -f compose.yaml -f compose.tunnel.yaml -f compose.dev-open.yaml \
  --profile tunnel --profile developer \
  up -d --no-build --no-deps --force-recreate tunnel-client

result_url=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$tunnel" | sed -n 's/^MCP_SERVER_URL=//p')
[[ "$result_url" == "$new_url" ]] || { echo "Open backend not applied" >&2; exit 1; }
ready=0
for attempt in $(seq 1 45); do
  if docker exec "$tunnel" tunnel-client health --port 8080 --json --require-control-plane-poll >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[[ "$ready" -eq 1 ]] || { echo "Tunnel never reached readiness and authenticated polling" >&2; exit 1; }
rollback_armed=0
echo "PILOT_OPEN_TUNNEL=VERIFIED_LOCAL"
echo "ChatGPT connector schema refresh and remote start_process/write_file remain PENDING."
echo "Reconnect the existing workstation-mcp-bridge test connector, not a new tunnel."
