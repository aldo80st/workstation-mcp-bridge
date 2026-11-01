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
- [x] Inspector CLI 2.13.0, ShellCheck 0.11.0 y Hadolint 2.14.0 **ejecutados en draft PR #23**, sin merge ([Inspector](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270504361), [linters](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270504232)).
- [x] Verificar detección real de fallo en CI: test sintético de PR #24 (cerrado, sin merge) hizo fallar ambos smoke ARM64/AMD64, [run 41270776887](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270776887). Esto no prueba bloqueo de merge.
- [ ] Revisar e integrar PR #23, evaluar CodeQL/Scorecard y demostrar check rojo **no fusionable** mediante ruleset main.
- [ ] Main ruleset/protección y required checks confirmados en GitHub (#18).
- [ ] SBOM, digest, inventario, scanner database/resultados de imagen **final** archivados.
- [ ] Revisión de backlog #2–#16/#18/#20 y aprobación expresa del responsable para merge/release.

Un workflow de seguridad successful significa que escaneó, no que los hallazgos fueron aceptados. Este repositorio no habilita publicación estable automática.
