# Security findings — local ARM64 pilot

Initial Bookworm image: 1 CRITICAL, 67 HIGH. Candidate Debian 13 image: 0 CRITICAL, 43 HIGH (Trivy 0.76.1). Counts reflect scanner/package instances, not proven exploit paths. Image ID: `sha256:96fdfadc0343671fb16a7f272abd6b03f14be4bf9b3971f1304ef2b7a46b4203`. Full local Trivy, SPDX SBOM and per-finding CSV are retained outside git. Updated CI must retain reports independently for its architecture/image.

## Critical zlib finding

CVE-2023-45853 appeared against Debian 12 zlib1g 1:1.2.13.dfsg-1. The [Debian tracker](https://security-tracker.debian.org/tracker/CVE-2023-45853) says Bookworm's src:zlib does not build affected contrib/minizip binaries. That is package-specific applicability evidence, not a blanket waiver. The candidate uses Debian 13 and the CRITICAL no longer appears; no suppression was added. Confirm final inventory separately if changing base or packaging.

## Remaining HIGH findings

| Package | HIGH instances | Scanner status | Fixed version | Assessment |
|---|---:|---|---|---|
| bsdutils | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libacl1 | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libblkid1 | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| liblastlog2-2 | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libmount1 | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libsmartcols1 | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libsystemd0 | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libtinfo6 | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libudev1 | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| libuuid1 | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| login | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| mount | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| ncurses-base | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| ncurses-bin | 1 | affected | not supplied | Requires per-CVE applicability review; no exception approved |
| perl-base | 1 | fix_deferred | not supplied | Requires per-CVE applicability review; no exception approved |
| util-linux | 4 | affected | not supplied | Requires per-CVE applicability review; no exception approved |

Non-root execution, no capabilities, no Docker socket, scoped mounts and memory/process limits reduce impact but do not prove these packages unexploitable. Open commands and file parsers increase reachable attack surface. These HIGH findings remain release blockers, not accepted risk. Do not infer safety from missing fixedVersion or a green advisory workflow.

## MCP and JavaScript dependencies

SDK 1.30.0 and split packages 2.0.0 generated high-severity findings. Lockfile overrides use SDK 1.32.0, client/server 2.3.0 and node 2.1.2; real initialize/list/call and profile regressions pass on ARM64. See [upstream advisory](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-46jr-4wx8-v453). Importantly, that advisory requires bounded tool input configuration in addition to upgrading; upgrading alone is not full remediation. Gateway body parsing still accepts up to 4 MiB and resource exhaustion remains a review item. Local loopback and container memory limits mitigate exposure; they do not close this finding.

Run npm audit separately: its database can flag issues absent from Trivy, including Zod collection validation. No unsupported Zod major override or automatic downgrade of Supergateway is applied just to obtain a green scan. Transitive vulnerabilities and upstream input bounds require follow-up before stable distribution. Runtime npm/npx are removed; dependency installation is build-only.

## Distribution and governance

Project original material uses MIT; dependencies retain their upstream licenses. Desktop Commander and Supergateway MIT license texts are included in NOTICE attachments. Complete transitive license/trademark review remains pending. Public rulesets endpoint returned an empty list during this audit; the public main branch API also returned `protected: false`. Issue #18 stays open. No main merge or stable release is authorized by this report.

## Per-CVE applicability triage (not approved exceptions)

| CVE | Evidence and local reachability | Disposition |
|---|---|---|
| CVE-2026-76642 | util-linux privileged post-mount helpers; non-root, all capabilities dropped and no-new-privileges prevent intended privileged mount path. Debian Trixie no-dsa/minor. | Conditional mitigation; no blanket waiver |
| CVE-2026-78408 | nsenter root cgroup descriptor inheritance; runtime does not start as root or run a privileged namespace helper. Debian no-dsa/minor. | Conditional mitigation; review Open command surface |
| CVE-2026-78409 | privileged X-mount.subdir symlink escape; no authorized privileged fstab mounts supplied. Debian no-dsa/minor. | Conditional mitigation; retain blocker |
| CVE-2026-78410 | privileged restricted bind source redirection; no capabilities or privileged fstab mounts. Debian no-dsa/minor. | Conditional mitigation; retain blocker |
| CVE-2026-54369 | libacl pathname race; requires a privileged caller operating on attacker-controlled paths. Runtime is non-root; Debian awaits point release/new ABI. | No privileged caller identified; library remains |
| CVE-2026-16742 | systemd-homed group privilege escalation; systemd-homed binary absent in inspected image. Libraries trigger scanner findings. Debian no-dsa/minor. | Candidate not-affected inventory evidence; reviewer approval pending |
| CVE-2025-69720 | infocmp parser overflow; infocmp is present. Restricted tools do not invoke it, Open can execute it as its own user. Debian no-dsa/minor. | Potential command surface; no exception approved |
| CVE-2026-9538 | Perl Archive::Tar memory exhaustion; importing Archive::Tar failed because module is absent. Debian postponed pending regression work. | Candidate not-affected inventory evidence; reviewer approval pending |

Primary source for each row: Debian Security Tracker at `https://security-tracker.debian.org/tracker/<CVE>`. Raw tracker responses, module/binary checks and full scanner package mapping are preserved in local evidence. Scanner HIGH classifications are retained, even where Debian rates impact lower. No suppressions or accepted VEX statements are shipped.
