# Sprint v0.1 — cierre de aceptación y Go/No-Go

Corte: **2026-10-31**. Base pública: `687d359afca4c96ee5bba3c325ac6ca63d1be971`. **Decisión: NO-GO para release estable, publicación de imágenes y merge a main.** El piloto Restricted/túnel existente puede continuar funcionando dentro de su alcance autorizado: funcionalidad E2E no equivale a producto liberable.

## Evidencia y límites

| Prueba / control | Resultado sustentado | Procedencia |
|---|---|---|
| Ubuntu 26.10 ARM64, Runtime Desktop Commander 0.3.1 + Supergateway 4.2.1, túnel 0.0.19, contenedores no privilegiados | Piloto local Restricted/loopback healthy previamente verificado | `docs/local-validation.md`, PR #21 |
| Pruebas funcionales y seguridad | 10 configuración, 11 Restricted, 8 startup y 4 Open; denegación directa, traversal, symlinks, read-only, health 503 ante fallo, cleanup Open→Restricted | `tests/`, `docs/local-validation.md`, PR #21; **no repetidas aquí** |
| Rollback | Imagen anterior pasó seis pruebas en proyecto desechable; retorno a imagen candidata pasó 11 Restricted | PR #21. La imagen anterior no está autorizada para desplegarse |
| ChatGPT por Secure MCP Tunnel | E2E real: `read_file /workspace/README.txt` entregó `MCP_SMOKE_FIXTURE`, `isError=false`, readiness/control-plane OK | PR #21 y confirmación del usuario; **sin publicar ID/clave** |
| Codex con complemento MCP | Lectura del mismo fixture reportada por el usuario | Prueba del cliente reportada; no implica compatibilidad universal |
| CI nativo | `smoke-amd64` y `smoke-arm64` **success** | [run 41267693747](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693747), reconsultado vía GitHub API |
| Escáneres y SBOM | `gitleaks-secrets` y `trivy-syft-sbom` **success**, **advisory** | [run 41267693756](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41267693756), API GitHub |
| Identidad de imagen ARM64 | `sha256:96fdfadc0343671fb16a7f272abd6b03f14be4bf9b3971f1304ef2b7a46b4203` | Evidencia local previa, no reconstruida en este corte |

**Acceso limitado en este corte:** el dispositivo Aldo_XPS se mostró offline y el conector directo cerró sesión; no se inspeccionó el checkout local `codex/sprint-closeout`, ni sus procesos Inspector ni los artefactos de revisores. Los informes adversarial y de licencias se deben **recuperar**, no asumir concluidos ni duplicar.

## Gates bloqueantes

1. **Seguridad #20/#14:** Trivy 0 CRITICAL / **43 HIGH** (ocho CVE); npm audit **3 HIGH / 12 MODERATE**; no hay excepciones generales aprobadas. El aviso [GHSA-46jr-4wx8-v453](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-46jr-4wx8-v453) exige límites de entrada y análisis de DoS además del upgrade SDK; Supergateway 4.2.1 usa límite JSON de 4 MiB. Exigir cambio mínimo, test RED/GREEN, suite y auditoría.
2. **Adversarial #14 y legal #4:** recuperar `docs/adversarial-review.md`, `docs/third-party-license-review.md`, `THIRD_PARTY_NOTICES.md` del trabajo local previo, verificar hallazgos y retests. SBOM de 771 registros, 23 NOASSERTION reportados previamente; licencias LGPL opcionales y metadatos sin declaración requieren evaluación individual. Ninguna revisión se considera aprobada.
3. **CI #7/#13:** [PR #23](https://github.com/aldo80st/workstation-mcp-bridge/pull/23) (draft) integra Inspector 2.13.0 con imagen fijada por digest, ShellCheck 0.11.0 y Hadolint 2.14.0 con checksums y fixtures negativos. Los jobs [Inspector](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270504361) y [linters](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270504232) pasaron en `59b648c`, **sin merge**. Faltan evaluación CodeQL/Scorecard y PR rojo **bloqueado por ruleset main**. La detección de fallo sí fue verificada: [run 41270776887](https://github.com/aldo80st/workstation-mcp-bridge/actions/runs/41270776887), PR #24 experimental **cerrado sin merge**, tuvo `smoke-arm64` y `smoke-amd64` fallidos al inyectar un test sintético con marcador `WMB_CI_NEGATIVE_DRILL_EXPECTED_FAILURE`; esto **no** prueba enforcement de reglas inexistentes.
4. **Gobernanza #18:** main sin ruleset/protección efectiva confirmada; configurar reglas y required checks desde cuenta administradora, después probar bloqueo real.
5. **Operación #15:** falta reinicio REAL del daemon Docker anfitrión. Hay dos contenedores ajenos: no reiniciarlos sin sudo y mantenimiento autorizado. Reiniciar el contenedor del piloto no satisface este criterio.
6. **Distribución #4/#16:** sign-off de licencias/notice/marca, CVE individual, SBOM+scan de candidato final, revisión independiente y autorización expresa para release/merge.

## Estado de issues (todos abiertos en la consulta)

| Issues | Situación | Faltante de aceptación |
|---|---|---|
| #2, #3 | Auditoría/arquitectura y Q-001 parcialmente demostrados | Comparar contrato/ADRs y cerrar amenazas con adversarial |
| #5, #6, #8, #9 | Núcleo, aislamiento, perfiles y Open→Restricted funcionales | Aceptación independiente + prueba de host no montado |
| #7, #10 | Suite MCP local; Inspector CLI probado en CI draft #23 | Revisión e integración; no prometer stdio sin prueba |
| #11, #12 | E2E túnel ChatGPT y lectura Codex reportados | Matriz final exacta por cliente y versión |
| #13 | CI nativo, escáneres, Inspector y linters probados en draft #23 | Review/merge, CodeQL/Scorecard y required checks de main (fallo de CI sí demostrado con PR #24 cerrado) |
| #14 | Revisiones delegadas, sin artefactos recuperados en este corte | Recuperar e inspeccionar informes/retests |
| #15 | Rollback/stop/start de contenedor | Ventana autorizada de restart del daemon |
| #4, #16, #18, #20 | **Bloqueantes** | Licencias, riesgos, branch rules y Go/No-Go final |

**Secuencia de cierre:** recuperar revisiones locales → RED/GREEN para límites de entrada y CI → resolver avisos/seguridad → administrador establece protección main → reinicio del daemon con ventana → reevaluar decisión con imagen, SHA, SBOM y retests finales. Ningún issue se cierra sólo porque el piloto funcione. No tag, release o merge.
