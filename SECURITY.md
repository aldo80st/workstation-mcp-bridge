# Security policy

Pilot software; do not treat v0.1 as production-approved. Report sensitive vulnerabilities privately to the repository maintainer through an available private GitHub security reporting channel. Do not put secrets or exploitable private deployment details into public issues.

Restricted denies mutating tools and uses a read-only workspace. It is not an egress sandbox. Open grants command execution under container permissions. Never expose anonymous MCP publicly, mount host root/home or Docker socket, or embed credentials in images. Local loopback clients are trusted local processes; use authenticated transport for remote access.

Known security blockers and scanner limitations are tracked in [security findings](docs/security-findings.md) and issue #20. There are no blanket CVE suppressions. Review final image and dependency scans before any stable publication.
