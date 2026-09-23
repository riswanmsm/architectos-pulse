# Lesson 1 • Example 04: Multi-Tenant OAuth2 JWT Security & Rate Limiting (`VBC-03`)

**Spec ID:** `SPEC-L1-EX04`  
**Component Target:** `COMP-SECURITY-GATEWAY` (`backend/app/services/security_gate.py`)  
**Database Entity:** `ENT-TENANT-POLICY` (`tenant_security_policies`)

---

## 1. Requirements (`requirements.md` — EARS Notation)

### FR-401: Mandatory OAuth2 Bearer JWT Verification
```text
WHEN a client invokes any protected `/api/*` or `/api/mcp/*` endpoint
THE SYSTEM SHALL validate the `Authorization: Bearer <jwt>` signature, expiration (`exp`), and `tenant_id` claim before executing controller logic.
```

### FR-402: Per-Tenant Sliding-Window Rate Limiting
```text
WHILE a tenant is issuing API or MCP tool requests
THE SYSTEM SHALL enforce a sliding-window rate limit of 100 requests per 60-second window per `tenant_id` and return HTTP `429 Too Many Requests` with a `Retry-After` header when exceeded.
```

### FR-403: Automatic Pre-Flight Vulnerability Rejection (`VBC-03`)
```text
IF an architecture specification or OpenAPI contract contains `placeholder auth`, `insecure`, or `no rate-limiting`
THEN THE SYSTEM SHALL raise a `Critical Finding`, force `ready = False`, cap `readiness_score <= 78`, and route remediation to `risk_engineering`.
```

### FR-404: Tenant Row-Level Isolation
```text
WHEN a database query executes against multi-tenant tables (`blueprint_sessions`, `vbc_verification_reports`)
THE SYSTEM SHALL scope all `SELECT`, `UPDATE`, and `DELETE` statements by the authenticated `tenant_id` UUID.
```

---

## 2. Technical Design (`design.md`)
- **Security Scheme:** OpenAPI 3.0 `BearerAuth` (`type: http`, `scheme: bearer`, `bearerFormat: JWT`).
- **Rate Limiter:** Token-bucket / sliding-window middleware keyed by `(tenant_id, route_path)`.

## 3. Implementation Tasks (`tasks.md`)
- [x] `TASK-401` (`FR-401`): Define OpenAPI `securitySchemes.BearerAuth` in `.kiro/specs/api.yaml`.
- [x] `TASK-402` (`FR-402`): Implement `429` rate-limit assertion check in `VBC-03` and `VBC-07`.
- [x] `TASK-403` (`FR-403`): Add property test `test_example_02_vbc_security_gate_invariants.py`.
- [x] `TASK-404` (`FR-404`): Add `tenant_id UUID NOT NULL` foreign keys to `.kiro/specs/schema.sql`.
