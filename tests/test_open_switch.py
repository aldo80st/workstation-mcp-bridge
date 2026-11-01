"""Static contract for the opt-in, reversible existing-tunnel Open switch.

Actual running-container, control-plane and ChatGPT acceptance remain separate.
"""
from pathlib import Path
import subprocess
import shutil
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "activate-open-pilot.sh"


def test_script_requires_existing_project_and_open_sidecar():
    assert SCRIPT.is_file(), "operator switch script not yet present"
    content = SCRIPT.read_text()
    for item in ("wmb-pilot", "wmb-pilot-workstation-mcp-open-1",
                 "MCP_DEV_WORKSPACE_PATH", "I_ACCEPT_OPEN_MODE_RISKS",
                 "tools/list", "start_process", "write_file", "read_file"):
        assert item in content


def test_switch_targets_single_tunnel_and_can_rollback():
    assert SCRIPT.is_file(), "operator switch script not yet present"
    source = SCRIPT.read_text()
    for item in ("wmb-pilot-tunnel-client-1", "--force-recreate",
                 "--no-deps", "--no-build",
                 "MCP_SERVER_URL=http://workstation-mcp:8765/mcp",
                 "rollback", "/var/run/docker.sock", "ChatGPT"):
        assert item in source
    assert "docker compose down" not in source
    assert "docker system prune" not in source

@pytest.mark.skipif(not shutil.which("bash"), reason="Bash is required for the operator script")
def test_script_has_valid_bash_syntax():
    assert SCRIPT.is_file()
    check = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
    assert check.returncode == 0, check.stderr
