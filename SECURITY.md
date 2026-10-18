# Security Policy 🔒 (URTC-DOCS)

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x  | ✅ Yes             |

## Reporting a Vulnerability

**CRITICAL: Do not report safety-critical vulnerabilities through public GitHub issues.**

This repository holds documents and small read-only tools; the code that moves machines lives in the other repositories of the ecosystem. What a report here can still be about:

1. **A document that says something unsafe or false**, for example a statement that a safety function exists or has been tested when it has not. These are the most serious findings: please say which sentence and which repository it contradicts.
2. **A tool that could leak or execute something**: the publication check reads git only, and the tools never run code of another repository except the `tools/ci_validate.py` that `tools/check_all.sh` starts in each one.
3. **A secret or private detail that reached a public file** of any repository of the ecosystem.

How to report:

1. **Email**: send a detailed report to `electrohobby3d@gmail.com`.
2. **Response**: initial acknowledgment within 48 hours.

We follow a coordinated disclosure policy so that hardware safety is addressed before a public release. The security posture of the ecosystem itself is described in `docs/SECURITY_BASELINE.md` and `docs/THREAT_MODEL.md`.
