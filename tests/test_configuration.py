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


def render_compose(*files, env=None):
    import json
    import os
    import subprocess
    args = ["docker", "compose"]
    for file in files:
        args.extend(["-f", str(ROOT / file)])
    return subprocess.run(args + ["--profile", "*", "config", "--format", "json"],
                          env={**os.environ, **(env or {})},
                          text=True, capture_output=True)


def test_tunnel_backend_can_be_overridden():
    import json
    result = render_compose("compose.yaml", "compose.tunnel.yaml", env={
        "CONTROL_PLANE_TUNNEL_ID": "tunnel_synthetic",
        "MCP_SERVER_URL": "http://authorized-backend:9000/custom"})
    assert result.returncode == 0, result.stderr
    config = json.loads(result.stdout)
    assert config["services"]["tunnel-client"]["environment"]["MCP_SERVER_URL"] == "http://authorized-backend:9000/custom"


def test_bind_mounts_never_create_missing_host_directories():
    import json
    for files, env in [(("compose.yaml",), {}),
                       (("compose.yaml", "compose.open.yaml"),
                        {"MCP_OPEN_WORKSPACE_PATH": "/synthetic/path"})]:
        result = render_compose(*files, env=env)
        assert result.returncode == 0, result.stderr
        import yaml
        mount = yaml.safe_load(read(files[-1]))["services"]["workstation-mcp"]["volumes"][0]
        assert mount["bind"]["create_host_path"] is False


def test_tunnel_secret_reader_uses_workspace_uid():
    import json
    result = render_compose('compose.yaml', 'compose.tunnel.yaml', env={
        'CONTROL_PLANE_TUNNEL_ID': 'tunnel_synthetic', 'MCP_UID': '1234', 'MCP_GID': '2345'})
    assert result.returncode == 0, result.stderr
    services = json.loads(result.stdout)['services']
    assert services['tunnel-client']['user'] == '1234:2345'
    assert services['workstation-mcp']['user'] == '1234:2345'
