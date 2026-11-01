# Changelog

## Unreleased — v0.1 stabilization

- Seed workspace-only Desktop Commander file policy and disable telemetry; regressions cover absolute/traversal/symlink/multiple-file reads.
- Verify MCP child health; reject reserved/invalid endpoint paths and malformed startup settings.
- Reject implicit bind-path creation; parameterize tunnel backend and align secret-reader UID/GID.
- Pin multi-platform base/tunnel digests and npm transitive dependencies; apply MCP SDK security patches and remove runtime npm tooling.
- Add negative calls, startup validation, profile switching and lifecycle evidence; document remaining security and E2E gates.
