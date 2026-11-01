import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_startup_seeds_workspace_policy_and_disables_telemetry(tmp_path):
    config = tmp_path / '.claude-server-commander/config.json'
    config.parent.mkdir()
    config.write_text('{"allowedDirectories":["/"],"telemetryEnabled":true}')
    result = subprocess.run(['node', str(ROOT / 'images/workstation-mcp/configure.mjs')],
                            env={**os.environ, 'HOME': str(tmp_path)}, capture_output=True)
    assert result.returncode == 0, result.stderr
    data = json.loads(config.read_text())
    assert data['allowedDirectories'] == ['/workspace']
    assert data['telemetryEnabled'] is False
