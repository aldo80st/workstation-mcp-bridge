# Release gates — corte 2026-10-31

**Decisión: NO-GO de publicación estable, imágenes y merge a main**. Ver [corte de aceptación](sprint-closeout-v0.1.md). La lectura E2E de ChatGPT es real y está demostrada, pero no resuelve los controles de distribución.

- [x] CI nativo AMD64/ARM64 y tests MCP/Restricted del candidato anterior ([run](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693747)).
- [x] E2E ChatGPT + Secure MCP Tunnel: lectura de fixture sintético, confirmado por usuario (PR #21).
- [x] Ejecución CI de Gitleaks, Trivy y Syft/SBOM ([run](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693756)); **advisory**, no dictamen de ausencia de CVE.
- [x] Rollback funcional de contenedor desechable y restauración Restricted; imagen anterior no aprobada para uso final.
- [ ] Reinicio del daemon Docker anfitrión en ventana autorizada, preservando servicios ajenos y verificando recuperación.
- [ ] Trivy 43 HIGH (ocho CVE), npm audit 3 HIGH/12 MODERATE, input/DoS GHSA con test RED/GREEN y revisión independiente aceptados.
- [ ] Recuperar informe adversarial, ejecutar/confirmar pruebas de abuso y retests.
- [ ] Inspeccionar licencias transitivas/LGPL, incertidumbres SBOM, THIRD_PARTY_NOTICES y marcas; sign-off distribución.
- [ ] Inspector CLI+CI, ShellCheck/Hadolint CI, evaluación CodeQL/Scorecard y demostración de check rojo bloqueante.
- [ ] Main ruleset/protección y required checks confirmados en GitHub (#18).
- [ ] SBOM, digest, inventario, scanner database/resultados de imagen **final** archivados.
- [ ] Revisión de backlog #2–#16/#18/#20 y aprobación expresa del responsable para merge/release.

Un workflow de seguridad successful significa que escaneó, no que los hallazgos fueron aceptados. Este repositorio no habilita publicación estable automática.
