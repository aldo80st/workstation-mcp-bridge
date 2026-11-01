# Release gates

Stable publication is blocked until all required evidence is attached to the final image digest:

- [ ] Updated native ARM64 and AMD64 CI and negative MCP regression tests.
- [ ] Real host Docker daemon restart and rollback validated in an approved maintenance window.
- [ ] Trivy HIGH findings classified individually and exploitable issues fixed or explicitly reviewed; npm audit findings reviewed separately.
- [ ] SBOM, exact image identity and scanner database/version retained with release artifacts.
- [ ] Secrets scan, ShellCheck/Hadolint and independent code/security review complete.
- [ ] ChatGPT tunnel E2E succeeds if that adapter is advertised as fully validated.
- [ ] LICENSE/NOTICE and transitive distribution obligations reviewed; name/brand clearance complete.
- [ ] main ruleset/protection and required checks verified by administrator (#18).
- [ ] Maintainer approval before merge or stable release.

Security workflow success means scanners ran and reports exist; vulnerability counts remain advisory for pilot development. It is not permission to publish a stable release. No stable-release publishing workflow is provided.
