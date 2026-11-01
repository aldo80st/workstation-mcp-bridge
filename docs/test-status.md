# Estado de pruebas — corte 2026-10-31

Referencia pública examinada: `687d359afca4c96ee5bba3c325ac6ca63d1be971`. Ver [corte de sprint](sprint-closeout-v0.1.md) y [validación local](local-validation.md).

- Local Ubuntu ARM64: **10** pruebas de configuración, **11** MCP Restricted, **8** startup, **4** Open, más reinicio, stop/start, Open→Restricted, limpieza tras fallo Open, health 503 y rollback funcional de proyecto desechable. **Estas pruebas fueron registradas anteriormente, no reejecutadas desde este chat.**
- CI de la referencia: [run 41267693747](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693747), `smoke-amd64` y `smoke-arm64` successful; [run 41267693756](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693756), `gitleaks-secrets` y `trivy-syft-sbom` successful. Escáner advisory **no** significa 0 HIGH.
- **ChatGPT E2E real:** túnel autorizado, readiness/control-plane OK, `read_file` del fixture sintético y `isError=false`, con confirmación del usuario. Codex también leyó el fixture según confirmación; esto no demuestra todos los clientes.
- Pendiente: Inspector CLI+CI; ShellCheck/Hadolint CI; evaluación CodeQL/Scorecard; CI negativo y required checks; revisión adversarial/licencias; límite de entrada+DoS RED/GREEN; 43 HIGH Trivy y 3 HIGH npm; protección main; reinicio real del daemon.

**Decisión actual: NO-GO estable.** No confundir éxito de piloto, sprint con criterios pendientes y release aprobada.
