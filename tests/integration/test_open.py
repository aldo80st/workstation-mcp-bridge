import json
import os
import unittest
from urllib.request import Request, urlopen

URL = os.environ.get("MCP_URL", "http://127.0.0.1:8765/mcp")

def mcp(method, params, ident):
    req = Request(URL, data=json.dumps({
        "jsonrpc": "2.0", "id": ident, "method": method, "params": params
    }).encode(), headers={
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2025-03-26",
    })
    with urlopen(req, timeout=45) as resp:
        data = resp.read().decode()
        if "text/event-stream" in resp.headers.get("Content-Type", ""):
            data = [line[5:].strip() for line in data.splitlines() if line.startswith("data:")][-1]
        return json.loads(data)

class OpenProfileTest(unittest.TestCase):
    def test_write_is_allowed_only_in_opt_in_profile(self):
        result = mcp("tools/call", {
            "name": "write_file",
            "arguments": {"path": "/workspace/allowed.txt", "content": "OPEN_SMOKE_OK"}
        }, 100)
        self.assertIn("result", result, result)

    def test_command_runs_inside_opted_in_workspace(self):
        result = mcp("tools/call", {
            "name": "start_process",
            "arguments": {"command": "sh -c 'printf WMB_OPEN_COMMAND_OK > /workspace/command.txt'"}
        }, 102)
        self.assertIn("result", result, result)

    def test_process_tool_is_discoverable(self):
        result = mcp("tools/list", {}, 101)
        self.assertIn("result", result, result)
        names = {item["name"] for item in result["result"]["tools"]}
        self.assertIn("start_process", names)

if __name__ == "__main__":
    unittest.main()
