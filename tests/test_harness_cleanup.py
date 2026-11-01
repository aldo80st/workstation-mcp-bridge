"""Exercise shell orchestration failure with a deliberately failing MCP test runner."""
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_failed_open_validation_restores_restricted(tmp_path):
    (tmp_path / 'scripts').mkdir()
    shutil.copy(ROOT / 'scripts/validate-local.sh', tmp_path / 'scripts/validate-local.sh')
    bins = tmp_path / 'bin'
    bins.mkdir()
    docker = bins / 'docker'
    docker.write_text('''#!/bin/sh
case "$*" in
  *compose.open.yaml*up*) printf open > "$WMB_STATE" ;;
  *"up -d"*) printf restricted > "$WMB_STATE" ;;
esac
''')
    python = bins / 'python3'
    python.write_text('''#!/bin/sh
case "$*" in *test_open.py*) exit 42;; esac
exit 0
''')
    docker.chmod(0o755)
    python.chmod(0o755)
    state = tmp_path / 'state'
    result = subprocess.run(['sh', str(tmp_path / 'scripts/validate-local.sh')],
                            env={**os.environ, 'PATH': str(bins) + os.pathsep + os.environ['PATH'],
                                 'WMB_STATE': str(state)}, capture_output=True)
    assert result.returncode == 42, result.stderr
    assert state.read_text() == 'restricted'
