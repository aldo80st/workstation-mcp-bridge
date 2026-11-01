# Test status — experimental

This project is not yet certified for public release. Use CI as the source of truth for each commit; a green run is not an independent penetration test.

## CI coverage
- GitHub-hosted Ubuntu amd64 and arm64 build and smoke.
- Default restricted Docker Compose configuration and Open opt-in guard.
- HTTP MCP initialize, tools/list, direct forbidden tools/call, permitted read_file.
- No tunnel-client credentials used in CI.

## Explicit gaps
- Real OpenAI Tunnel ID and API key E2E: untested until user-authorized temporary credentials.
- Open mode runtime shell/write: must be tested only against a disposable mounted workspace.
- Security scanner (Trivy/Gitleaks/Syft), upstream license/SBOM and brand review: pending.
- Ubuntu native XPS: not tested because connected remote agent was offline when this work started.
- CI does not prove absence of Docker escape or malicious user content prompt-injection.
