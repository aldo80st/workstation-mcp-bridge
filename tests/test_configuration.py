from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text()

def test_default_profile_restricted():
    assert "MCP_SECURITY_PROFILE: restricted" in read("compose.yaml")
    assert "read_only: true" in read("compose.yaml")
    assert "--tools read_file" in read("images/workstation-mcp/entrypoint.sh")

def test_open_requires_explicit_ack():
    code = read("images/workstation-mcp/entrypoint.sh")
    assert 'I_ACCEPT_OPEN_MODE_RISKS' in code
    assert 'MCP_OPEN_ACK' in code
    assert "MCP_OPEN_WORKSPACE_PATH:?" in read("compose.open.yaml")

def test_no_default_privilege_escalation():
    compose = read("compose.yaml")
    assert "cap_drop: [ALL]" in compose
    assert "no-new-privileges:true" in compose
    assert "127.0.0.1:" in compose
    assert "docker.sock" not in compose
    assert "privileged: true" not in compose

def test_tunnel_is_optional_and_key_as_file():
    tunnel = read("compose.tunnel.yaml")
    assert 'profiles: ["tunnel"]' in tunnel
    assert "file:/run/secrets/control-plane-api-key" in tunnel
    assert "CONTROL_PLANE_TUNNEL_ID" in tunnel
    assert "CONTROL_PLANE_API_KEY:" not in tunnel

def test_no_provider_dependency_in_default_compose():
    assert "openai" not in read("compose.yaml").lower()
    assert "tunnel-client" not in read("compose.yaml")
