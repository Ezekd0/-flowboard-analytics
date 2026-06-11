# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 1.x | Yes |
| 0.x | No |

## Reporting a Vulnerability

Please report vulnerabilities privately to:

- Email: `[your-email]`
- Subject: `TaskFlow Analytics Security Report`

Include:
- impacted component and version
- reproducible steps or proof-of-concept
- severity assessment (if known)
- potential mitigation ideas

Do not open public issues for vulnerabilities.

## Security Measures Implemented

- [x] JWT-based authentication with configurable expiration
- [x] Password hashing via bcrypt
- [x] Environment-driven secrets and config isolation
- [x] Input validation with Pydantic schemas
- [x] Configurable API rate limiting
- [x] Reverse proxy security headers in NGINX
- [x] Dependency pinning strategy for critical packages
- [x] Structured logging for audit and incident triage

## Disclosure Policy

1. Report received and acknowledged within 72 hours.
2. Initial triage and impact assessment within 7 days.
3. Patch development and validation timeline shared privately.
4. Public disclosure coordinated after patch release and user notification.

## Hall of Fame

We appreciate responsible disclosure. Contributors who report valid issues may be listed here (with permission):

- `[Researcher Name]` - `[Advisory ID or short description]`
