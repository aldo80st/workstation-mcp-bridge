# Matriz de clientes — corte 2026-10-31

Evidencias de `687d359afca4c96ee5bba3c325ac6ca63d1be971`, [PR #21](https://github.com/aldo80st/workstation-mcp-bridge/pull/21) y el usuario. **NO-GO** para distribución; cada afirmación indica su alcance.

| Cliente | OS/arquitectura | Transporte | Estado / evidencia |
|---|---|---|---|
| Harness Python urllib | Ubuntu 26.10 ARM64 | MCP streamable HTTP 2025-03-26, loopback | **tested**: initialize, list, read, direct deny, malformed; `tests/integration/test_mcp.py` |
| CI nativo | Ubuntu runner AMD64 y ARM64 | Streamable HTTP, entorno aislado | **tested**: [41267693747](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693747) |
| Node fetch probe | Debian ARM64 | Docker private HTTP | **tested parcial**: initialize, evidencia local previa |
| Tunnel-client 0.0.19 | Linux ARM64 | Docker backend HTTP, Secure MCP Tunnel opcional | **tested**: pruebas sintéticas de startup y E2E real vía ChatGPT |
| ChatGPT (complemento privado) | Cuenta autorizada | Secure MCP Tunnel real | **tested E2E**: `read_file /workspace/README.txt` devuelve `MCP_SMOKE_FIXTURE`, `isError=false`; usuario confirmó |
| Codex (complemento conectado) | XPS Ubuntu 26.10 ARM64 | MCP remoto | **tested reportado**: lectura del mismo fixture; sin matriz completa |
| MCP Inspector 2.13.0 | Inst. iniciada en checkout interrumpido | Por comprobar | **pending**: falta ejecución CLI y CI |
| Claude / Cursor / VS Code / otros | No probado | No afirmado | **not-tested** |

Open sólo se probó con workspace sintético desechable, **no** con ChatGPT. Manifest multi-arquitectura no equivale a interoperabilidad universal.
