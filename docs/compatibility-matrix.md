# Compatibility matrix

| Client/test | OS/CPU | Transport/auth | Evidence/status |
|---|---|---|---|
| Python urllib JSON-RPC harness | Ubuntu 26.10 ARM64 | Streamable HTTP 2025-03-26 / local loopback | initialize, list, read, negative calls verified locally |
| Container Node fetch probe | Debian container ARM64 | Docker bridge HTTP / private bridge | recorded separately in local evidence |
| GitHub Actions native smoke | Linux ARM64 + AMD64 | Streamable HTTP / isolated runner | original 9efbea3 passed run 41266050115; updated commit requires new CI |
| tunnel-client 0.0.19 | Linux ARM64 | internal HTTP + synthetic identity | CLI, secret-file startup and local error handling; no external E2E claim |
| ChatGPT through Secure MCP Tunnel | target account | authorized tunnel | pending real credentials and representative tool call |
| MCP Inspector/other clients | not tested | not asserted | pending |

The pinned base and tunnel manifest include ARM64/AMD64. Manifest support does not prove runtime behavior. No universal compatibility claim.
