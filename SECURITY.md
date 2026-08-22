# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x.x   | ✅ Active support |
| 1.x.x   | ❌ End of life |

---

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in ADPilot Pro, please follow responsible disclosure practices.

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities.
2. **Email** your report to: **gharieb@adpilot.dev**
3. Include the following in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected file(s), branch, and commit hash
   - Potential impact assessment
   - Suggested mitigation (if known)

### What to Expect

| Timeline | Action |
|----------|--------|
| **24 hours** | Acknowledgment of your report |
| **72 hours** | Initial assessment and severity classification |
| **7 days** | Remediation plan communicated |
| **30 days** | Fix deployed (critical/high severity) |

### Severity Classification

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Remote code execution, data exfiltration | API key exposure, SQL injection |
| **High** | Authentication bypass, privilege escalation | HITL gate bypass, unauthorized approval |
| **Medium** | Information disclosure, CSRF | Verbose error messages, debug endpoints in production |
| **Low** | Minor information leakage | Version disclosure, missing security headers |

---

## Security Architecture

ADPilot Pro implements multiple layers of security:

### Secrets Management
- All API keys and credentials are managed via `.env` files.
- `.env` is listed in `.gitignore` and **never** committed to the repository.
- Only `.env.example` (with placeholder values) is tracked.
- If a key is leaked, rotate it **immediately** and notify the maintainer.

### Cryptographic Governance (HITL)
- High-risk actions (budget changes > $1,000, live campaign publishing) are quarantined behind the **Human-in-the-Loop** governance gate.
- Every approval/rejection generates an **HMAC-SHA256 signed audit receipt**.
- Signatures are computed over: `CampaignID || Decision || Timestamp || Role`.

### Input Validation
- All external inputs pass through **Pydantic v2 strict-mode validation** before entering the agent pipeline.
- No raw unvalidated data can reach any AI agent.

### API Security
- **CORS middleware** with configurable allowed origins.
- **Rate limiting** on all public endpoints.
- No sensitive data in API error responses in production mode.

### Data Protection
- No real customer data in sample files or test fixtures.
- No private business data, emails, phone numbers, or addresses in tracked files.
- Use placeholder values in all JSON samples and documentation examples.

---

## Security Contacts

- **Primary**: [@GhariebML](https://github.com/GhariebML)
- **Email**: gharieb@adpilot.dev

---

<p align="center">
  <em>Thank you for helping keep ADPilot Pro secure.</em>
</p>
