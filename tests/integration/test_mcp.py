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
        self.assertTrue("error" in payload or payload.get("http_status", 0) >= 400, payload)

    def test_nonmounted_host_data_is_inaccessible(self):
        payload = mcp("tools/call", {
            "name": "read_file",
            "arguments": {"path": "/tmp/wmb-ci-host-secret.txt"}
        }, reqid=5)
        self.assertNotIn("WMB_HOST_SECRET_MARKER", json.dumps(payload))

    def test_allowed_read_call(self):
        payload = mcp("tools/call", {
            "name": "read_file",
            "arguments": {"path": "/workspace/README.txt"}
        }, reqid=4)
        self.assertIn("result", payload, payload)
        self.assertIn("MCP_SMOKE_FIXTURE", json.dumps(payload["result"]))

if __name__ == "__main__":
    unittest.main()
