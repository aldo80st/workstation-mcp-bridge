import json
import os
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError

URL = os.environ.get("MCP_URL", "http://127.0.0.1:8765/mcp")

def mcp(method, params=None, reqid=1):
    payload = {"jsonrpc": "2.0", "id": reqid, "method": method}
    if params is not None:
        payload["params"] = params
    request = Request(URL, data=json.dumps(payload).encode(), headers={
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2025-03-26",
    })
    try:
        with urlopen(request, timeout=45) as response:
            data = response.read().decode("utf-8")
            ctype = response.headers.get("Content-Type", "")
    except HTTPError as error:
        return {"http_status": error.code, "body": error.read().decode()}
    if "text/event-stream" in ctype:
        events = [line[5:].strip() for line in data.splitlines()
                  if line.startswith("data:") and line[5:].strip() != "[DONE]"]
        if not events:
            return {"raw": data}
        return json.loads(events[-1])
    return json.loads(data)

class MCPContractTest(unittest.TestCase):
    def test_initialize(self):
        result = mcp("initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "wmb-ci", "version": "0.1"},
        })
        self.assertIn("result", result, result)
        self.assertIn("serverInfo", result["result"])

    def test_restricted_discovery(self):
        tools = mcp("tools/list", reqid=2)
        self.assertIn("result", tools, tools)
        names = {x["name"] for x in tools["result"]["tools"]}
        self.assertIn("read_file", names)
        self.assertNotIn("start_process", names)
        self.assertNotIn("write_file", names)

    def test_restricted_denies_direct_write_call(self):
        payload = mcp("tools/call", {
            "name": "write_file",
            "arguments": {"path": "/workspace/forbidden.txt", "content": "should-not-exist"}
        }, reqid=3)
        self.assertEqual(payload.get("error", {}).get("code"), -32602, payload)

    def test_nonmounted_host_data_is_inaccessible(self):
        payload = mcp("tools/call", {
            "name": "read_file",
            "arguments": {"path": "/tmp/wmb-ci-host-secret.txt"}
        }, reqid=5)
        self.assertNotIn("WMB_HOST_SECRET_MARKER", json.dumps(payload))

    def test_direct_process_tool_denied(self):
        payload = mcp("tools/call", {
            "name": "start_process",
            "arguments": {"command": "touch /workspace/prohibited-command-marker"}
        }, reqid=6)
        self.assertEqual(payload.get("error", {}).get("code"), -32602, payload)

    def test_reads_outside_workspace_are_denied(self):
        for path in ("/etc/passwd", "/workspace/../etc/passwd", "/workspace/outside-link"):
            with self.subTest(path=path):
                payload = mcp("tools/call", {"name": "read_file", "arguments": {"path": path}})
                self.assertIn("result", payload, payload)
                self.assertTrue(payload["result"].get("isError"), payload)
                self.assertIn("Path not allowed", json.dumps(payload))
                self.assertNotIn("root:x:", json.dumps(payload))

    def test_multiple_reads_cannot_escape_workspace(self):
        payload = mcp("tools/call", {"name": "read_multiple_files",
                      "arguments": {"paths": ["/workspace/README.txt", "/etc/passwd"]}})
        self.assertIn("MCP_SMOKE_FIXTURE", json.dumps(payload))
        self.assertIn("Path not allowed", json.dumps(payload))
        self.assertNotIn("root:x:", json.dumps(payload))

    def test_alternate_mutation_tools_are_denied(self):
        for name in ("edit_block", "move_file", "set_config_value", "create_directory", "interact_with_process"):
            with self.subTest(name=name):
                payload = mcp("tools/call", {"name": name, "arguments": {}})
                self.assertEqual(payload.get("error", {}).get("code"), -32602, payload)

    def test_unknown_method_returns_protocol_error(self):
        payload = mcp("wmb/unknown", {})
        self.assertEqual(payload.get("error", {}).get("code"), -32601, payload)

    def test_malformed_json_is_rejected(self):
        request = Request(URL, data=b'{broken', headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as caught:
            urlopen(request, timeout=10)
        self.assertEqual(caught.exception.code, 400)
        caught.exception.close()

    def test_allowed_read_call(self):
        payload = mcp("tools/call", {
            "name": "read_file",
            "arguments": {"path": "/workspace/README.txt"}
        }, reqid=4)
        self.assertIn("result", payload, payload)
        self.assertIn("MCP_SMOKE_FIXTURE", json.dumps(payload["result"]))

if __name__ == "__main__":
    unittest.main()
