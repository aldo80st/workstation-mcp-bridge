"""Regression: daemon restarts do not apply Compose dependency ordering."""
import json

from test_configuration import render_compose


def test_tunnel_waits_for_mcp_before_discovery_after_daemon_restart():
    result = render_compose("compose.yaml", "compose.tunnel.yaml", env={
        "CONTROL_PLANE_TUNNEL_ID": "tunnel_synthetic",
    })
    assert result.returncode == 0, result.stderr
    services = json.loads(result.stdout)["services"]
    tunnel = services["tunnel-client"]
    # The pinned client's opt-in wait gates BOTH initialize and OAuth discovery;
    # depends_on alone only orders Compose up, not Docker's restart manager.
    assert tunnel["environment"].get("MCP_STARTUP_WAIT_TIMEOUT") == "120s"
    assert tunnel["environment"]["MCP_SERVER_URL"] == "http://workstation-mcp:8765/mcp"
    assert services["workstation-mcp"]["environment"]["MCP_SECURITY_PROFILE"] == "restricted"
