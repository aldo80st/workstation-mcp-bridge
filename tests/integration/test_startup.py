"""Container startup validation; requires a built local image and Docker access."""
import os
import subprocess
import unittest

IMAGE = os.environ.get('WMB_IMAGE', 'workstation-mcp-bridge:local')


class StartupTest(unittest.TestCase):
    def reject(self, **variables):
        command = ['docker', 'run', '--rm']
        for key, value in variables.items():
            command.extend(['-e', f'{key}={value}'])
        # A stub ensures an invalid value cannot start a listening server.
        command += ['--entrypoint', 'sh', IMAGE, '-c',
                    'mkdir -p /tmp/bin; printf "#!/bin/sh\\nexit 0\\n" > /tmp/bin/supergateway; '
                    'chmod +x /tmp/bin/supergateway; PATH=/tmp/bin:$PATH exec wmb-entrypoint']
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 64, result.stderr)

    def test_reserved_health_path_is_rejected(self):
        self.reject(MCP_PATH='/healthz')

    def test_health_aliases_are_rejected(self):
        for path in ('/Healthz', '/healthz/', '/HEALTHZ///'):
            with self.subTest(path=path):
                self.reject(MCP_PATH=path)

    def test_dot_segments_are_rejected(self):
        self.reject(MCP_PATH='/mcp/./v1')

    def test_control_character_in_path_is_rejected(self):
        self.reject(MCP_PATH='/mcp\tother')

    def test_unknown_profile_is_rejected(self):
        self.reject(MCP_SECURITY_PROFILE='unexpected')

    def test_open_requires_acknowledgement(self):
        self.reject(MCP_SECURITY_PROFILE='open')

    def test_invalid_ports_are_rejected(self):
        for value in ('0', '1023', '65536', '-1', 'abc'):
            with self.subTest(value=value):
                self.reject(MCP_PORT=value)

    def test_missing_key_file_is_rejected(self):
        self.reject(MCP_API_KEY_FILE='/missing-key')


if __name__ == '__main__':
    unittest.main()
