"""Contract for optional, isolated Open-mode development access.

These tests intentionally precede the overlay/script (TDD RED) and then
exercise the actual Docker Compose model on GitHub native ARM64/AMD64 CI.
No credentials or user-specific filesystem paths are checked in.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "compose.dev-open.yaml"
SCRIPT = ROOT / "scripts" / "dev-open.sh"


def test_open_sidecar_has_no_host_port_or_privileged_mounts():
    assert OVERLAY.is_file(), "Open development overlay not yet implemented"
    document = yaml.safe_load(OVERLAY.read_text())
    service = document["services"]["workstation-mcp-open"]
    assert "developer" in service["profiles"]
    assert service["image"] == "workstation-mcp-bridge:local"
    assert "build" not in service
    assert not service.get("ports"), "Open sidecar must be Docker-network-only"
    assert service["environment"]["MCP_SECURITY_PROFILE"] == "open"
    assert service["environment"]["MCP_OPEN_ACK"] == "${MCP_OPEN_ACK:-}"
    assert service["cap_drop"] == ["ALL"]
    assert "no-new-privileges:true" in service["security_opt"]
    assert service["pids_limit"] <= 128
    assert service["mem_limit"] == "1g"
    mount, = service["volumes"]
    assert mount["target"] == "/workspace"
    assert mount["read_only"] is False
    assert mount["bind"]["create_host_path"] is False
    assert mount["source"].startswith("${MCP_DEV_WORKSPACE_PATH:?")
    assert not any(item in str(service) for item in
                   ("docker.sock", "privileged: true", "/var/run", "/home/amarquez"))

    tunnel = document["services"]["tunnel-client"]
    assert tunnel["environment"]["MCP_SERVER_URL"].startswith(
        "http://workstation-mcp-open:"), "Reuse existing tunnel credentials; do not create a second tunnel"


def test_switch_is_opt_in_and_preserves_restricted_fallback():
    assert SCRIPT.is_file(), "Reversible activation script not yet implemented"
    script = SCRIPT.read_text()
    assert "I_ACCEPT_OPEN_MODE_RISKS" in script
    assert "workstation-mcp-open" in script
    assert "workstation-mcp" in script
    assert "tunnel-client" in script
    assert "--force-recreate" in script
    assert "--no-deps" in script
    assert "docker compose down" not in script
    assert "docker system prune" not in script
    assert "sudo " not in script
    assert "docker.sock" in script  # explicitly rejected mount exposure in comments/contracts


@pytest.mark.skipif(not shutil.which("docker"), reason="Docker Compose is tested in hosted native runners")
def test_rendered_open_contract_and_tunnel_backend():
    env = {**os.environ,
           "MCP_DEV_WORKSPACE_PATH": str(ROOT),
           "MCP_OPEN_ACK": "I_ACCEPT_OPEN_MODE_RISKS",
           "CONTROL_PLANE_TUNNEL_ID": "tunnel_synthetic"}
    args = ["docker", "compose"]
    for item in ("compose.yaml", "compose.tunnel.yaml", "compose.dev-open.yaml"):
        args.extend(["-f", str(ROOT / item)])
    result = subprocess.run(
        args + ["--profile", "developer", "--profile", "tunnel", "config", "--format", "json"],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=45)
    assert result.returncode == 0, result.stderr
    services = json.loads(result.stdout)["services"]
    restricted = services["workstation-mcp"]
    opened = services["workstation-mcp-open"]
    tunnel = services["tunnel-client"]
    assert restricted["environment"]["MCP_SECURITY_PROFILE"] == "restricted"
    assert restricted["volumes"][0]["read_only"] is True
    assert opened["environment"]["MCP_SECURITY_PROFILE"] == "open"
    assert opened["volumes"][0]["read_only"] is False
    assert opened.get("ports") is None
    assert tunnel["environment"]["MCP_SERVER_URL"] == "http://workstation-mcp-open:8765/mcp"
    assert tunnel["secrets"], "Tunnel continues to read existing secret file"
